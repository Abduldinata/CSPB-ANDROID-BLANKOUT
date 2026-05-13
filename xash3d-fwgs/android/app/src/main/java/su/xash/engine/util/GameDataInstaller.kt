package su.xash.engine.util

import android.content.Context
import android.content.res.AssetManager
import java.io.File
import java.io.FileOutputStream
import java.io.IOException

data class InstallProgress(
	val current: Int,
	val total: Int,
	val path: String,
)

object GameDataInstaller {
	private const val BUFFER_SIZE = 1024 * 1024

	fun getDefaultGameRoot(ctx: Context): File {
		// Android/data/<pkg>/files (easy to locate via ADB; no runtime storage permission required).
		return ctx.getExternalFilesDir(null) ?: ctx.filesDir
	}

	fun isGameFolderReady(dir: File, isValve: Boolean): Boolean {
		if (!dir.isDirectory) return false
		val gameinfo = File(dir, "gameinfo.txt")
		val liblist = File(dir, "liblist.gam")
		if (!gameinfo.isFile || !liblist.isFile) return false

		// Minimal sanity: a few required subfolders exist.
		return if (isValve) {
			File(dir, "resource").isDirectory && File(dir, "gfx").isDirectory
		} else {
			File(dir, "gfx").isDirectory && File(dir, "addons").isDirectory && File(dir, "scripts").isDirectory
		}
	}

	@Throws(IOException::class)
	fun ensureInstalled(
		ctx: Context,
		root: File,
		onProgress: (InstallProgress) -> Unit = {},
	) {
		val cspbDir = File(root, "cspb")
		val valveDir = File(root, "valve")

		val needCspb = !isGameFolderReady(cspbDir, isValve = false)
		val needValve = !isGameFolderReady(valveDir, isValve = true)
		if (!needCspb && !needValve) return

		val assetManager = ctx.assets
		val total = (if (needCspb) countFiles(assetManager, "cspb") else 0) +
			(if (needValve) countFiles(assetManager, "valve") else 0)

		var current = 0
		if (needCspb) {
			copyAssetTree(assetManager, "cspb", cspbDir, overwrite = false) { path ->
				current++
				val rel = path.removePrefix("cspb/").ifBlank { path }
				onProgress(InstallProgress(current, total, "cspb/$rel"))
			}
		}
		if (needValve) {
			copyAssetTree(assetManager, "valve", valveDir, overwrite = false) { path ->
				current++
				val rel = path.removePrefix("valve/").ifBlank { path }
				onProgress(InstallProgress(current, total, "valve/$rel"))
			}
		}
	}

	private fun countFiles(am: AssetManager, assetPath: String): Int {
		val entries = am.list(assetPath) ?: return 0
		if (entries.isEmpty()) return 1
		var count = 0
		for (name in entries) {
			count += countFiles(am, "$assetPath/$name")
		}
		return count
	}

	@Throws(IOException::class)
	private fun copyAssetTree(
		am: AssetManager,
		assetPath: String,
		dest: File,
		overwrite: Boolean,
		onFileCopied: (String) -> Unit,
	) {
		val entries = am.list(assetPath) ?: return
		if (entries.isEmpty()) {
			copyAssetFile(am, assetPath, dest, overwrite)
			onFileCopied(assetPath)
			return
		}

		if (!dest.exists() && !dest.mkdirs()) {
			throw IOException("Failed to create dir: ${dest.absolutePath}")
		}

		for (name in entries) {
			val childAsset = "$assetPath/$name"
			val childDest = File(dest, name)
			copyAssetTree(am, childAsset, childDest, overwrite, onFileCopied)
		}
	}

	@Throws(IOException::class)
	private fun copyAssetFile(am: AssetManager, assetPath: String, destFile: File, overwrite: Boolean) {
		if (destFile.exists() && !overwrite) return
		destFile.parentFile?.mkdirs()
		am.open(assetPath).use { input ->
			FileOutputStream(destFile).use { output ->
				input.copyTo(output, bufferSize = BUFFER_SIZE)
			}
		}
	}
}
