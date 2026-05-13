import com.android.build.api.dsl.ApplicationExtension

import java.time.LocalDateTime
import java.time.Month
import java.time.temporal.ChronoUnit
import java.util.Properties

plugins {
	alias(libs.plugins.android.application)
}

extensions.configure<ApplicationExtension> {
	namespace = "su.xash.engine"
	ndkVersion = "30.0.14904198"
	compileSdk = 34

	// Optional release signing (kept out of git):
	// Create `android/keystore.properties` (see `android/keystore.properties.example`).
	// If missing, `release` will be produced as `app-release-unsigned.apk` (current Gradle default behavior).
	val keystoreProps = Properties()
	val keystorePropsFile = project.rootProject.file("keystore.properties")
	val hasReleaseSigning = keystorePropsFile.exists()
	if (hasReleaseSigning) {
		keystoreProps.load(keystorePropsFile.inputStream())
	}

	defaultConfig {
		applicationId = "com.cspb.blankout"
		versionName = "1.0"
		versionCode = getBuildNum()
		minSdk = 21
		targetSdk = 29

		val localProperties = Properties()
		val localPropFile = project.rootProject.file("local.properties")
		if (localPropFile.exists()) {
			localProperties.load(localPropFile.inputStream())
		}
		val sdkDir = localProperties.getProperty("sdk.dir", "")
		val safeNdkRoot = localProperties.getProperty("ndk.dir", "$sdkDir/ndk/30.0.14904198").replace("\\", "/")

		externalNativeBuild {
			val engineRoot = projectDir.parentFile.parent

			experimentalProperties["ninja.abiFilters"] = setOf("arm64-v8a")
			experimentalProperties["ninja.path"] = File(engineRoot, "wscript").path
			experimentalProperties["ninja.configure"] = "run-python"
			experimentalProperties["ninja.arguments"] = setOf(
				File(engineRoot, "scripts/configure-ninja.py").path,
				engineRoot,
				"--variant=\${ndk.variantName}",
				"--abi=arm64-v8a",
				"--configuration-dir=\${ndk.buildRoot}",
				"--ndk-version=\${ndk.moduleNdkVersion}",
				"--min-sdk-version=\${ndk.minPlatform}",
				"--ndk-root=${safeNdkRoot}",
				// shut up, fake options
				"-p:Configuration=\${ndk.variantName}",
				"-p:Platform=arm64-v8a"
			)
		}
	}

	compileOptions {
		sourceCompatibility = JavaVersion.VERSION_17
		targetCompatibility = JavaVersion.VERSION_17
	}

	buildFeatures {
		viewBinding = true
		buildConfig = true
	}

	lint {
		abortOnError = false
		checkReleaseBuilds = false
		disable.add("ExpiredTargetSdkVersion")
	}

/*
	androidResources {
		noCompress += ""
	}
*/

	packaging {
		jniLibs {
			keepDebugSymbols.add("**/*.so")
			useLegacyPackaging = true
			excludes.add("**/armeabi-v7a/**")
			// Removed to ensure CSPB client is packaged properly
			// excludes.add("**/arm64-v8a/libclient_android_arm64.so")
		}
	}

	sourceSets {
		getByName("main") {
			// Launcher-only APK: keep engine extras, but do not package project game data.
			assets.srcDirs("src/main/assets", "../../3rdparty/extras/xash-extras")
			java.srcDirs("src/main/java", "../../3rdparty/SDL/android-project/app/src/main/java")
		}
	}

	if (hasReleaseSigning) {
		signingConfigs {
			create("release") {
				val storeFilePath = keystoreProps.getProperty("storeFile")?.trim()
				require(!storeFilePath.isNullOrEmpty()) { "keystore.properties: storeFile is missing" }

				// Resolve relative paths from the Android root project (xash3d-fwgs/android),
				// not from the app module directory.
				storeFile = project.rootProject.file(storeFilePath)
				storePassword = keystoreProps.getProperty("storePassword")
				keyAlias = keystoreProps.getProperty("keyAlias")
				keyPassword = keystoreProps.getProperty("keyPassword")
			}
		}
	}

	buildTypes {
		debug {
			isMinifyEnabled = false
			isShrinkResources = false
			isDebuggable = true
			proguardFiles(
				getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
			)
		}

		release {
			isMinifyEnabled = true
			isShrinkResources = true
			if (hasReleaseSigning) {
				signingConfig = signingConfigs.getByName("release")
			}
			proguardFiles(
				getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
			)
		}

		register("asan") {
			initWith(getByName("debug"))
		}

		register("continuous") {
			initWith(getByName("release"))
			isMinifyEnabled = false
			isShrinkResources = false
			signingConfig = signingConfigs.getByName("debug")
		}
	}
}

dependencies {
	implementation(libs.material)

	implementation(libs.appcompat)
	implementation(libs.navigation.runtime.ktx)
	implementation(libs.navigation.fragment.ktx)
	implementation(libs.navigation.ui.ktx)
	implementation(libs.preference.ktx)
	implementation(libs.swiperefreshlayout)

	implementation(libs.acra.http)
}

fun getBuildNum(): Int {
	val now = LocalDateTime.now()
	val releaseDate = LocalDateTime.of(2015, Month.APRIL, 1, 0, 0, 0)
	val qBuildNum = releaseDate.until(now, ChronoUnit.DAYS)
	val minuteOfDay = now.hour * 60 + now.minute
	return (qBuildNum * 10000 + minuteOfDay).toInt()
}

fun getGitHash(): String {
	val process = ProcessBuilder("git", "rev-parse", "--short", "HEAD").directory(project.rootDir)
		.redirectErrorStream(true).start()
	return process.inputStream.bufferedReader().readText().trim()
}

// Kotlin plugin is applied by Android Gradle Plugin in this project setup.

// Workaround for intermittent/dirty-state failures like:
// Zip file '*.png.jar' already contains entry '...png', cannot overwrite
// Ensure compressed_assets intermediates are cleared before the Android Gradle Plugin compressAssets tasks run.
tasks
	.matching { it.name.startsWith("compress") && it.name.endsWith("Assets") }
	.configureEach {
		doFirst {
			delete(layout.buildDirectory.dir("intermediates/compressed_assets"))
		}
	}
