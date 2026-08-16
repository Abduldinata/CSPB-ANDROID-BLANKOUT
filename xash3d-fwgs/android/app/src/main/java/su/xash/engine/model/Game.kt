package su.xash.engine.model

import android.content.Context
import android.content.Intent
import android.content.pm.PackageInfo
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import androidx.core.net.toUri
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import su.xash.engine.R
import su.xash.engine.XashActivity
import java.io.File
import java.io.FileInputStream
import java.util.Arrays
import android.util.Log

class Game(val ctx: Context, val basedir: File, val gameInfoFile: File) {
	private var iconName = "icon.png"
	var title = "Unknown Game"
	var icon: Bitmap? = null
	var cover: Bitmap? = null

	val mobileHacksGames = arrayOf("aom", "bdlands", "biglolly", "bshift", "caseclosed",
		"hl_urbicide", "induction", "redempt", "secret",
		"sewer_beta", "tot", "valve", "vendetta")

	// a1ba: follow the behavior of Xash3D's game_launch.
	// for hl mods we put `valve` as game directory
	// for any other game that's not hl this string must be replaced with your
	// main game directory
	// mods always use -game command line parameter
	var defaultGameDir = "valve"

	private val pref = ctx.getSharedPreferences(basedir.name, Context.MODE_PRIVATE)

	init {
		try {
			parseGameInfo(gameInfoFile)
		} catch (e: Exception) {
			e.printStackTrace()
		}

		if (basedir.name.equals("cspb", ignoreCase = true)) {
			defaultGameDir = basedir.name
			icon = BitmapFactory.decodeResource(ctx.resources, R.drawable.cspb_game_logo)
		}

		if (icon == null) {
			val iconCandidates = linkedSetOf(
				iconName,
				"icon.png",
				"game.ico",
				"cstrike.ico"
			)

			for (candidate in iconCandidates) {
				val iconFile = File(basedir, candidate)
				if (iconFile.exists()) {
					icon = BitmapFactory.decodeFile(iconFile.path)
					if (icon != null) {
						break
					}
				}
			}
		}

		try {
			cover = BackgroundBitmap.createBackground(basedir)
		} catch (e: Exception) {
			e.printStackTrace()
		}
	}

	fun startEngine(ctx: Context) {
		val packageNames = getPackageNamesForGameDir(basedir.name)
		var externalGame = false
		var commandLineArgs = "";
		val isCspb = basedir.name.equals("cspb", ignoreCase = true)

		if (isCspb) {
			Log.i("XASH_DIAG", "CSPB_LAUNCH_REV 2026-05-09A diagnostics=off medkit_skip_expected args_pref=" + (pref.getString("arguments", "") ?: ""))
		}

		if (basedir.name != defaultGameDir)
			commandLineArgs += "-game ${basedir.name} "

		if (packageNames != null) {
			if (packageNames.contains(ctx.packageName)) {
				commandLineArgs += "-dll @hl "
			} else if (packageNames.contains("su.xash.cs16client")) {
				if (pref.getBoolean("enable_yapb_bots", true)) {
					commandLineArgs += "-dll @yapb "
				}
				externalGame = true
			}
		}

		// Fallback removed - we now compile the CSPB arm64 server gamedll natively

		// Keep launch args light for CSPB Android recovery builds.
		// Old installs may have diagnostics persisted in SharedPreferences,
		// so don't trust the stored flag here.
		val diagnosticsEnabled = false
		var userArgs = pref.getString("arguments", if (isCspb) "" else "-console") ?: if (isCspb) "" else "-console"

		// User often types -dev2 (without space), but engine expects -dev 2.
		userArgs = userArgs.replace("-dev2", "-dev 2")
		if (isCspb) {
			// Force CSPB-specific launch args and strip stale overrides from old launcher configs.
			userArgs = userArgs.replace(Regex("(^|\\s)-console(?=\\s|$)"), "$1")
			userArgs = userArgs.replace(Regex("(^|\\s)-clientlib\\s+\\S+"), "$1")
			userArgs = userArgs.replace(Regex("(^|\\s)-serverlib\\s+\\S+"), "$1")
			userArgs = userArgs.replace(Regex("(^|\\s)-dll\\s+\\S+"), "$1")
			userArgs = userArgs.replace(Regex("(^|\\s)-game\\s+\\S+"), "$1")
			userArgs = userArgs.replace(Regex("(^|\\s)-log\\s+\\S+"), "$1")
			userArgs = userArgs.replace(Regex("\\s+"), " ").trim()
			userArgs += " -clientlib libcspb_client_android_arm64.so -serverlib libcspb_server_android_arm64.so"
		}
		val argTokens = userArgs.trim().split(Regex("\\s+")).filter { it.isNotBlank() }
		val hasDev = argTokens.contains("-dev")

		if (diagnosticsEnabled) {
			if (!hasDev) {
				userArgs += " -dev 3"
			}
			Log.i("XASH_DIAG", "Phase 1 Diagnostics enabled: $userArgs")
			if (isCspb) {
				Log.i("XASH_DIAG", "CSPB game detected. Expected assets: sprites/*.txt, models/player/*.mdl, models/w_*.mdl, sound/weapons/*.wav")
			}
		}

		if (!pref.getBoolean("sound_enabled", true)) {
			userArgs += " -nosound"
		}

		if (pref.getBoolean("use_custom_resolution", false)) {
			val customWidth = pref.getString("custom_width", "")?.trim().orEmpty().toIntOrNull()
			val customHeight = pref.getString("custom_height", "")?.trim().orEmpty().toIntOrNull()
			if (customWidth != null && customWidth > 0 && customHeight != null && customHeight > 0) {
				userArgs += " -width $customWidth -height $customHeight"
			}
		}

		commandLineArgs += " -heapsize 524288 -client_heapsize 262144"
		commandLineArgs += " $userArgs"

		var packageName: String? = null
		var gameLibDir: String? = null
		if (externalGame && packageNames != null) {
			for (pn in packageNames) {
				gameLibDir = try {
					getGameLibDir(ctx, pn)
				} catch(e: PackageManager.NameNotFoundException) {
					null
				} catch(e: Exception) {
					e.printStackTrace()
					null
				}

				if (gameLibDir != null) {
					packageName = pn
					break
				}
			}

			if (gameLibDir == null) {
				MaterialAlertDialogBuilder(ctx).apply {
					setTitle(R.string.game_apk_required)
					setMessage(R.string.game_apk_message)
					setPositiveButton(R.string.game_apk_install) { _, _ ->
						val intent = Intent(Intent.ACTION_VIEW,
							getDownloadPageForGameDir(basedir.name).toUri())
						ctx.startActivity(intent)
					}
					show()

					return
				}
			}
		}

		ctx.startActivity(Intent(ctx, XashActivity::class.java).apply {
			flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK

			putExtra("gamedir", if (isCspb) basedir.name else defaultGameDir)
			putExtra("argv", commandLineArgs)
			putExtra("usevolume", pref.getBoolean("use_volume_buttons", false))
			//putExtra("keyboardresizescreen", pref.getBoolean("keyboard_resizes_screen", true))
			putExtra("keyboardresizescreen", pref.getBoolean("keyboard_resizes_screen", false))
			putExtra("basedir", basedir.parent)

			if (gameLibDir != null) {
				putExtra("gamelibdir", gameLibDir)
			}

			putExtra("package", packageName ?: ctx.packageName)
		})
	}

	private fun parseGameInfo(file: File) {
		FileInputStream(file).use { inputStream ->
			inputStream.bufferedReader().use { reader ->
				reader.forEachLine {
					val tokens = it.split("\\s+".toRegex(), limit = 2)
					if (tokens.size >= 2) {
						val k = tokens[0]
						val v = tokens[1].trim('"')

						if (k == "title" || k == "game") title = v
						if (k == "icon") iconName = v
					}
				}
			}
		}
	}

	private fun getPackageNamesForGameDir(gamedir: String): Array<String>? {
		if (gamedir.equals("cstrike", ignoreCase = true)
			|| gamedir.equals("czero", ignoreCase = true))
			return arrayOf("su.xash.cs16client.test", "su.xash.cs16client")

		if (gamedir.equals("tfc", ignoreCase = true))
			return arrayOf("su.xash.tf15client.test", "su.xash.tf15client")

		// mobile_hacks hlsdk-portable branch allows us to have few more mods out of the box
		if (mobileHacksGames.any { it.equals(gamedir, ignoreCase = true) })
			return arrayOf(ctx.packageName)

        // return if (mDbEntry != null) {
        //    mDbEntry.getPackageName()
        // } else null
		return null
	}

	private fun getDownloadPageForGameDir(gamedir: String): String {
		if (gamedir.equals("cstrike", ignoreCase = true)
			|| gamedir.equals("czero", ignoreCase = true))
			return "https://github.com/Velaron/cs16-client/releases/download/continuous/CS16Client-Android.apk"

		if (gamedir.equals("tfc", ignoreCase = true))
			return "https://github.com/Velaron/tf15-client/releases/download/continuous/TF15Client-Android.apk"

		// just so we don't return null
		return "https://github.com/FWGS/xash3d-fwgs/releases/download/continuous/xash3d-fwgs-android.apk"
	}

	private fun getGameLibDir(ctx: Context, packageName: String): String? {
		val packageInfo: PackageInfo = ctx.packageManager.getPackageInfo(packageName, 0)
		return packageInfo.applicationInfo?.nativeLibraryDir
	}

	companion object {
		fun getGames(ctx: Context, root: File): List<Game> {
			val games = mutableListOf<Game>()

			root.listFiles()?.forEach {
				if (it.isDirectory) {
					val subDirGameInfoFile = checkIfGamedir(it)
					if (subDirGameInfoFile != null) {
						try {
							games.add(Game(ctx, it, subDirGameInfoFile))
						} catch (e: Exception) {
							e.printStackTrace()
						}
					}
				}
			}

			return games
		}

		fun checkIfGamedir(gamedir: File): File? {
			gamedir.listFiles()?.forEach {
				if (it.isFile) {
					if (it.name.equals("liblist.gam", ignoreCase = true))
						return it

					if (it.name.equals("gameinfo.txt", ignoreCase = true))
						return it
				}
			}

			return null
		}
	}
}
