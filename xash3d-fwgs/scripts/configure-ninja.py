#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2025 Velaron
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from __future__ import print_function

import argparse
import os
import subprocess
import sys
import io
import shutil


def check_repo(name, branch, url, path):
	if not os.path.exists(path):
		print("{} not found. Cloning...".format(name))
		git_exec = ["git", "clone", "--branch", branch, url, path]
		git_process = subprocess.Popen(git_exec)
		git_process.communicate()


def run_cmake(root, out, toolchain, abi, build_type, ndk_root, min_sdk, *args):
	cache_file = os.path.join(out, "CMakeCache.txt")
	if os.path.isfile(cache_file):
		with io.open(cache_file, "r", encoding="utf-8", errors="ignore") as f:
			cache_text = f.read()
		# Recreate broken configure output so CMake can pick up the Ninja path we provide now.
		if "CMAKE_MAKE_PROGRAM:FILEPATH=CMAKE_MAKE_PROGRAM-NOTFOUND" in cache_text:
			shutil.rmtree(out, ignore_errors=True)

	cmake_bin = shutil.which("cmake")
	ninja_bin = shutil.which("ninja")
	if not cmake_bin:
		# Try to locate CMake in the Android SDK (common on Windows setups).
		sdk_root = os.path.abspath(os.path.join(ndk_root, os.pardir, os.pardir))
		cmake_root = os.path.join(sdk_root, "cmake")
		if os.path.isdir(cmake_root):
			versions = [d for d in os.listdir(cmake_root) if os.path.isdir(os.path.join(cmake_root, d))]
			versions.sort(reverse=True)
			for v in versions:
				candidate = os.path.join(cmake_root, v, "bin", "cmake.exe" if os.name == "nt" else "cmake")
				if os.path.isfile(candidate):
					cmake_bin = candidate
					# Ninja is shipped alongside CMake in the Android SDK.
					if not ninja_bin:
						ninja_candidate = os.path.join(cmake_root, v, "bin", "ninja.exe" if os.name == "nt" else "ninja")
						if os.path.isfile(ninja_candidate):
							ninja_bin = ninja_candidate
					break

	if not cmake_bin:
		raise RuntimeError("cmake not found in PATH and not found under Android SDK cmake/")

	cmake_exec = [cmake_bin, "-H{}".format(root),
		"-DCMAKE_BUILD_TYPE={}".format(build_type),
		"-DCMAKE_TOOLCHAIN_FILE={}".format(toolchain),
		"-DANDROID_ABI={}".format(abi),
		"-DANDROID_NDK={}".format(ndk_root),
		"-DANDROID_PLATFORM=android-{}".format(min_sdk),
		"-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
		"-DCMAKE_SYSTEM_NAME=Android",
		"-DCMAKE_SYSTEM_VERSION={}".format(min_sdk),
		"-B{}".format(out), "-GNinja"]

	if ninja_bin:
		cmake_exec.append("-DCMAKE_MAKE_PROGRAM={}".format(ninja_bin))

	cmake_exec.extend(args)
	cmake_process = subprocess.Popen(cmake_exec)
	cmake_process.communicate()
	if cmake_process.returncode != 0:
		raise RuntimeError("cmake configure failed for {}".format(root))


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("wscript_path")
	parser.add_argument("--variant")
	parser.add_argument("--abi")
	parser.add_argument("--configuration-dir")
	parser.add_argument("--ndk-version")
	parser.add_argument("--min-sdk-version")
	parser.add_argument("--ndk-root")

	args, unknown = parser.parse_known_args()

	abi = args.abi

	cmake_build_type = "Debug" if args.variant in ["debug", "asan"] else "Release"
	cmake_toolchain_path = os.path.join(args.ndk_root, "build", "cmake", "android.toolchain.cmake")

	# configure SDL2
	sdl_path = os.path.join(args.wscript_path, "3rdparty", "SDL")
	check_repo("SDL", "release-2.32.8", "https://github.com/libsdl-org/SDL", sdl_path)

	sdl_out_path = os.path.join(args.configuration_dir, "SDL")

	run_cmake(sdl_path, sdl_out_path, cmake_toolchain_path, abi, cmake_build_type, args.ndk_root, args.min_sdk_version,
			  "-DSDL_RENDER=OFF", "-DSDL_POWER=OFF", "-DSDL_VULKAN=OFF", "-DSDL_DISKAUDIO=OFF",
			  "-DSDL_DUMMYAUDIO=OFF", "-DSDL_DUMMYVIDEO=OFF",
			  "-DSDL_VULKAN=OFF", "-DSDL_OFFSCREEN=OFF", "-DSDL_STATIC=OFF")

	# configure hlsdk-portable
	hlsdk_path = os.path.join(args.wscript_path, "3rdparty", "hlsdk-portable")
	check_repo("hlsdk-portable", "mobile_hacks", "https://github.com/FWGS/hlsdk-portable", hlsdk_path)

	hlsdk_out_path = os.path.join(args.configuration_dir, "hlsdk-portable")

	run_cmake(hlsdk_path, hlsdk_out_path, cmake_toolchain_path, abi, cmake_build_type, args.ndk_root,
			  args.min_sdk_version, "-DANDROID_APK=ON")

	# configure mainui_cpp
	mainui_path = os.path.join(args.wscript_path, "3rdparty", "mainui")
	mainui_out_path = os.path.join(args.configuration_dir, "mainui")

	run_cmake(mainui_path, mainui_out_path, cmake_toolchain_path, abi, cmake_build_type, args.ndk_root,
		args.min_sdk_version, "-DBUILD_AS_PART_OF_ENGINE=ON")

	# waf configure
	waf_path = os.path.join(args.wscript_path, "waf")
	out_path = os.path.join(args.configuration_dir, "xash3d-fwgs")

	waf_build_type = "debug" if args.variant in ["debug", "asan"] else "release"

	env = os.environ.copy()
	env["WAFLOCK"] = ".lock-waf_android_{}_build".format(abi)
	env["ANDROID_NDK"] = args.ndk_root
	env["BUILD_CMAKE_LIBRARY_OUTPUT_DIRECTORY"] = sdl_out_path

	waf_exec = [sys.executable, waf_path, "configure", "-t", args.wscript_path, "-o", out_path,
				"-T", waf_build_type, "--android={},,{}".format(abi, args.min_sdk_version), "-s",
				sdl_path, "--skip-sdl2-sanity-check", "--enable-bundled-deps", "--disable-soft", "ninja"]

	process = subprocess.Popen(waf_exec, env=env)
	process.communicate()
	if process.returncode != 0:
		return process.returncode

	with io.open(os.path.join(args.configuration_dir, "build.ninja.txt"), "w", encoding="utf-8") as f:
		f.write(os.path.join(out_path, "build.ninja"))

	# required for Android Studio
	return 0


if __name__ == "__main__":
	sys.exit(main())
