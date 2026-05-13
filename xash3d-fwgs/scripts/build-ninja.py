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

import argparse
import os
import shutil
import subprocess
import sys


def run_cmake(bin_path, libs, inst_path):
	cmake_bin = shutil.which("cmake")
	if not cmake_bin:
		android_sdk = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT")
		if not android_sdk and os.name == "nt":
			default_sdk = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk")
			if os.path.isdir(default_sdk):
				android_sdk = default_sdk
		if android_sdk:
			cmake_root = os.path.join(android_sdk, "cmake")
			if os.path.isdir(cmake_root):
				versions = [d for d in os.listdir(cmake_root) if os.path.isdir(os.path.join(cmake_root, d))]
				versions.sort(reverse=True)
				for version in versions:
					candidate = os.path.join(cmake_root, version, "bin", "cmake.exe" if os.name == "nt" else "cmake")
					if os.path.isfile(candidate):
						cmake_bin = candidate
						break

	if not cmake_bin:
		raise RuntimeError("cmake not found in PATH and not found under Android SDK cmake/")

	cmake_exec = [cmake_bin, "--build", bin_path]
	cmake_process = subprocess.Popen(cmake_exec)
	cmake_process.communicate()
	if cmake_process.returncode != 0:
		raise RuntimeError("cmake --build failed for {}".format(bin_path))

	if libs:
		for lib in libs:
			src = os.path.join(bin_path, *lib.split("/"))
			dest = os.path.join(inst_path, lib.split("/")[-1])

			dest_dir = os.path.dirname(dest)

			if not os.path.exists(dest_dir):
				os.makedirs(dest_dir)

			shutil.copyfile(src, dest)
	else:
		cmake_exec = [cmake_bin, "--install", bin_path, "--prefix", inst_path]
		cmake_process = subprocess.Popen(cmake_exec)
		cmake_process.communicate()
		if cmake_process.returncode != 0:
			raise RuntimeError("cmake --install failed for {}".format(bin_path))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("cmd")
	parser.add_argument("top_dir")
	parser.add_argument("out_dir")
	parser.add_argument("waflock")
	parser.add_argument("--targets", type=str, default="")

	args = parser.parse_args()

	waf_path = os.path.join(args.top_dir, "waf")

	env = os.environ.copy()
	env["WAFLOCK"] = args.waflock

	waf_exec = [sys.executable, waf_path, args.cmd, "-t", args.top_dir]

	if args.targets:
		waf_exec += ["--targets={}".format(args.targets)]
	else:
		# build SDL2 and hlsdk-portable with cmake
		sdl_bin_path = os.path.join(args.out_dir, "SDL")
		hlsdk_bin_path = os.path.join(args.out_dir, "hlsdk-portable")
		mainui_bin_path = os.path.join(args.out_dir, "mainui")

		abi = args.waflock.replace(".lock-waf_android_", "").replace("_build", "")
		inst_path = os.path.join(args.top_dir, "android", "app", "src", "main", "jniLibs", abi)

		if not os.path.exists(inst_path):
			os.makedirs(inst_path)

		run_cmake(sdl_bin_path, ["libSDL2.so"], inst_path)
		run_cmake(hlsdk_bin_path, None, inst_path)
		run_cmake(mainui_bin_path, None, inst_path)

	process = subprocess.Popen(waf_exec, env=env)
	process.communicate()
	return process.returncode

if __name__ == "__main__":
	sys.exit(main())
