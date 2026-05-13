pluginManagement {
	repositories {
		google {
			content {
				includeGroupByRegex("com\\.android.*")
				includeGroupByRegex("com\\.google.*")
				includeGroupByRegex("androidx.*")
			}
		}
		mavenCentral()
		gradlePluginPortal()
	}
}

// NOTE(CSPB): disable Foojay toolchain resolver.
// It tries to download JetBrains Runtime 21 from api.foojay.io and may fail (HTTP 400)
// depending on network environment. We use the locally-installed JDK instead.

dependencyResolutionManagement {
	repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
	repositories {
		google()
		mavenCentral()
	}
}

rootProject.name = "Xash3D FWGS"
include(":app")
