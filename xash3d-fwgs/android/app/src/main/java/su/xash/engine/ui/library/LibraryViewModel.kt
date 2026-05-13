package su.xash.engine.ui.library

import android.app.Application
import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.os.Build
import android.os.Environment
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import su.xash.engine.model.Game
import su.xash.engine.util.Nomedia
import java.io.File
import java.io.IOException

class LibraryViewModel(application: Application) : AndroidViewModel(application) {
	companion object {
		private const val BUNDLED_DATA_VERSION_KEY = "bundled_data_version"
		private const val USE_BUNDLED_DATA_SYNC = false
		private const val USE_LEGACY_DATA_MIGRATION = false
	}

	data class DataSyncProgress(
		val phase: String,
		val doneFiles: Int,
		val totalFiles: Int,
		val current: String? = null
	) {
		val percent: Int
			get() = if (totalFiles <= 0) 0 else ((doneFiles * 100) / totalFiles).coerceIn(0, 100)
	}

	val installedGames: LiveData<List<Game>> get() = _installedGames
	private val _installedGames = MutableLiveData(emptyList<Game>())

	val isReloading: LiveData<Boolean> get() = _isReloading
	private val _isReloading = MutableLiveData(false)

	val dataSyncProgress: LiveData<DataSyncProgress?> get() = _dataSyncProgress
	private val _dataSyncProgress = MutableLiveData<DataSyncProgress?>(null)

	val selectedItem: LiveData<Game> get() = _selectedItem
	private val _selectedItem = MutableLiveData<Game>()

	private val appPreferences: SharedPreferences =
		application.getSharedPreferences("app_preferences", Context.MODE_PRIVATE)

	fun reloadGames(ctx: Context) {
		if (isReloading.value == true) {
			return
		}
		_isReloading.value = true

		viewModelScope.launch {
			withContext(Dispatchers.IO) {
				try {
					val app = getApplication<Application>()
					val baseFilesRoot = app.getExternalFilesDir(null)?.absolutePath
						?: (Environment.getExternalStorageDirectory().absolutePath + "/Android/data/${app.packageName}/files")
					val defaultRoot = baseFilesRoot
					val rootPath = defaultRoot
					val root = File(rootPath)
					if (!root.exists()) {
						root.mkdirs()
					}
					if (USE_BUNDLED_DATA_SYNC) {
						syncBundledGameDataIfNeeded(app, root)
					}
					if (USE_LEGACY_DATA_MIGRATION) {
						migrateLegacyFoldersIfNeeded(root, File(baseFilesRoot))
					}
					File(root, "cspb").mkdirs()
					File(root, "valve").mkdirs()
					appPreferences.edit().putString("game_path", rootPath).apply()

					Nomedia.ensureNomedia(root)

					_installedGames.postValue(Game.getGames(ctx, root))
				} catch (e: Exception) {
					e.printStackTrace()
					_installedGames.postValue(emptyList())
					_dataSyncProgress.postValue(null)
				} finally {
					_isReloading.postValue(false)
				}
			}
		}
	}

	fun setSelectedGame(game: Game) {
		_selectedItem.value = game
	}

	fun startEngine(ctx: Context, game: Game) {
		game.startEngine(ctx)
	}

	private fun migrateLegacyFoldersIfNeeded(root: File, filesRoot: File) {
		val legacyRoot = File(Environment.getExternalStorageDirectory(), "xash")
		if (legacyRoot.exists() && legacyRoot.isDirectory) {
			migrateLegacyFolder(legacyRoot, root, "cspb")
			migrateLegacyFolder(legacyRoot, root, "valve")
		}

		// If data already exists at files/v16/cspb or files/v16/valve, move/copy into files/cspb and files/valve.
		val legacyVersionRoot = File(filesRoot, "v16")
		if (legacyVersionRoot.exists() && legacyVersionRoot.isDirectory) {
			migrateLegacyFolder(legacyVersionRoot, root, "cspb")
			migrateLegacyFolder(legacyVersionRoot, root, "valve")
		}

		// Also accept content already placed directly in files/cspb or files/valve.
		migrateLegacyFolder(filesRoot, root, "cspb")
		migrateLegacyFolder(filesRoot, root, "valve")
	}

	private fun syncBundledGameDataIfNeeded(ctx: Context, root: File) {
		val assetVersion = getCurrentAssetVersion(ctx)
		val installedVersion = appPreferences.getLong(BUNDLED_DATA_VERSION_KEY, Long.MIN_VALUE)

		if (installedVersion == assetVersion &&
			File(root, "cspb").exists() &&
			File(root, "valve").exists()) {
			return
		}

		val leaves = mutableListOf<String>()
		leaves.addAll(listAssetLeafFilesIfExists(ctx, "cspb"))
		leaves.addAll(listAssetLeafFilesIfExists(ctx, "valve"))

		val total = leaves.size
		var done = 0
		_dataSyncProgress.postValue(DataSyncProgress("Copying resources", 0, total, null))

		copyAssetTreeIfExists(ctx, "cspb", File(root, "cspb")) {
			done += 1
			_dataSyncProgress.postValue(DataSyncProgress("Copying resources", done, total, it))
		}
		copyAssetTreeIfExists(ctx, "valve", File(root, "valve")) {
			done += 1
			_dataSyncProgress.postValue(DataSyncProgress("Copying resources", done, total, it))
		}

		appPreferences.edit().putLong(BUNDLED_DATA_VERSION_KEY, assetVersion).apply()
		_dataSyncProgress.postValue(null)
	}

	private fun getCurrentAssetVersion(ctx: Context): Long {
		val packageInfo = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
			ctx.packageManager.getPackageInfo(ctx.packageName, PackageManager.PackageInfoFlags.of(0))
		} else {
			@Suppress("DEPRECATION")
			ctx.packageManager.getPackageInfo(ctx.packageName, 0)
		}

		return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
			packageInfo.longVersionCode
		} else {
			@Suppress("DEPRECATION")
			packageInfo.versionCode.toLong()
		}
	}

	private fun copyAssetTreeIfExists(
		ctx: Context,
		assetPath: String,
		destination: File,
		onFileCopied: ((String) -> Unit)? = null
	) {
		val entries = try {
			ctx.assets.list(assetPath)
		} catch (e: IOException) {
			return
		} ?: return

		if (entries.isEmpty()) {
			copyAssetFile(ctx, assetPath, destination)
			onFileCopied?.invoke(assetPath)
			return
		}

		if (!destination.exists()) {
			destination.mkdirs()
		}

		entries.forEach { entry ->
			copyAssetTreeIfExists(ctx, "$assetPath/$entry", File(destination, entry), onFileCopied)
		}
	}

	private fun copyAssetFile(ctx: Context, assetPath: String, destination: File) {
		destination.parentFile?.mkdirs()
		ctx.assets.open(assetPath).use { input ->
			destination.outputStream().use { output ->
				input.copyTo(output)
			}
		}
	}

	private fun migrateLegacyFolder(legacyRoot: File, newRoot: File, folderName: String) {
		val source = File(legacyRoot, folderName)
		if (!source.exists() || !source.isDirectory) {
			return
		}

		val destination = File(newRoot, folderName)
		if (destination.exists() && destination.listFiles()?.isNotEmpty() == true) {
			return
		}

		copyRecursive(source, destination)
	}

	private fun copyRecursive(source: File, destination: File) {
		if (source.isDirectory) {
			if (!destination.exists()) {
				destination.mkdirs()
			}

			source.listFiles()?.forEach { child ->
				copyRecursive(child, File(destination, child.name))
			}
			return
		}

		destination.parentFile?.mkdirs()
		source.inputStream().use { input ->
			destination.outputStream().use { output ->
				input.copyTo(output)
			}
		}
	}

	private fun listAssetLeafFilesIfExists(ctx: Context, assetPath: String): List<String> {
		val entries = try {
			ctx.assets.list(assetPath)
		} catch (e: IOException) {
			return emptyList()
		} ?: return emptyList()

		if (entries.isEmpty()) {
			return listOf(assetPath)
		}

		val out = ArrayList<String>(entries.size)
		entries.forEach { entry ->
			out.addAll(listAssetLeafFilesIfExists(ctx, "$assetPath/$entry"))
		}
		return out
	}
}
