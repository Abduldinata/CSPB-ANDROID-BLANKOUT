package su.xash.engine;

import android.annotation.SuppressLint;
import android.content.pm.ActivityInfo;
import android.content.res.AssetManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.Settings.Secure;
import android.util.Log;
import android.view.KeyEvent;
import android.view.WindowManager;

import org.libsdl.app.SDLActivity;

import su.xash.engine.util.AndroidBug5497Workaround;
import su.xash.engine.util.GameNotification;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

public class XashActivity extends SDLActivity {
	private boolean mUseVolumeKeys;
	private boolean mKeyboardResizesScreen;
	private String mPackageName;
	private static final String TAG = "XashActivity";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		checkAndExtractGameAssets();

		String basedir = getIntent().getStringExtra("basedir");
		if (basedir != null && !basedir.isEmpty()) {
			try {
				android.system.Os.setenv("XASH3D_BASEDIR", basedir, true);
			} catch (Exception e) {
				Log.e(TAG, "Failed to set XASH3D_BASEDIR: " + e.getMessage());
			}
		} else {
			File externalFiles = getExternalFilesDir(null);
			if (externalFiles != null && new File(externalFiles, "cspb").exists()) {
				try {
					android.system.Os.setenv("XASH3D_BASEDIR", externalFiles.getAbsolutePath(), true);
				} catch (Exception e) {
					Log.e(TAG, "Failed to set default XASH3D_BASEDIR: " + e.getMessage());
				}
			}
		}

		super.onCreate(savedInstanceState);
		mKeyboardResizesScreen = getIntent().getBooleanExtra("keyboardresizescreen", false);

		setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE);
		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
			getWindow().getAttributes().layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
		}

		if (mKeyboardResizesScreen) {
			AndroidBug5497Workaround.assistActivity(this);
		}

		startLogcatCapture();
	}

	private void checkAndExtractGameAssets() {
		try {
			File externalFiles = getExternalFilesDir(null);
			if (externalFiles == null) return;

			File gameDir = new File(externalFiles, "cspb");
			File marker = new File(gameDir, ".installed_version");
			int currentVersion = BuildConfig.VERSION_CODE;

			boolean needsExtract = !gameDir.exists() || !new File(gameDir, "gameinfo.txt").exists();
			if (!needsExtract && marker.exists()) {
				try (java.io.BufferedReader reader = new java.io.BufferedReader(new java.io.FileReader(marker))) {
					int savedVersion = Integer.parseInt(reader.readLine().trim());
					if (savedVersion < currentVersion) {
						needsExtract = true;
					}
				} catch (Exception e) {
					needsExtract = true;
				}
			} else {
				needsExtract = true;
			}

			if (needsExtract) {
				Log.i(TAG, "Checking bundled game assets for extraction to " + gameDir.getAbsolutePath());
				AssetManager am = getAssets();
				String[] bundledList = am.list("cspb");
				if (bundledList != null && bundledList.length > 0) {
					Log.i(TAG, "Bundled 'cspb' assets detected (" + bundledList.length + " root items). Starting auto-import...");
					if (!gameDir.exists()) {
						gameDir.mkdirs();
					}
					copyAssetFolder(am, "cspb", gameDir);

					try (java.io.FileWriter writer = new java.io.FileWriter(marker)) {
						writer.write(String.valueOf(currentVersion));
					}
					Log.i(TAG, "Auto-import complete! All game data extracted successfully.");
				} else {
					Log.i(TAG, "No bundled 'cspb' assets inside APK; using existing files in external storage.");
				}
			}
		} catch (Exception e) {
			Log.e(TAG, "Error checking/extracting game assets: " + e.getMessage(), e);
		}
	}

	private static boolean copyAssetFolder(AssetManager assetManager, String fromAssetPath, File toDir) {
		try {
			String[] files = assetManager.list(fromAssetPath);
			if (files == null || files.length == 0) {
				return copyAssetFile(assetManager, fromAssetPath, toDir);
			} else {
				if (!toDir.exists()) {
					toDir.mkdirs();
				}
				boolean ok = true;
				for (String file : files) {
					String subFrom = fromAssetPath.isEmpty() ? file : fromAssetPath + "/" + file;
					File subTo = new File(toDir, file);

					String[] subFiles = assetManager.list(subFrom);
					if (subFiles != null && subFiles.length > 0) {
						if (!subTo.exists()) subTo.mkdirs();
						ok &= copyAssetFolder(assetManager, subFrom, subTo);
					} else {
						ok &= copyAssetFile(assetManager, subFrom, subTo);
					}
				}
				return ok;
			}
		} catch (Exception e) {
			Log.e(TAG, "Failed to copy asset folder: " + fromAssetPath, e);
			return false;
		}
	}

	private static boolean copyAssetFile(AssetManager assetManager, String fromAssetPath, File toFile) {
		try (InputStream in = assetManager.open(fromAssetPath);
		     OutputStream out = new FileOutputStream(toFile)) {
			byte[] buffer = new byte[65536];
			int read;
			while ((read = in.read(buffer)) != -1) {
				out.write(buffer, 0, read);
			}
			out.flush();
			return true;
		} catch (Exception e) {
			Log.e(TAG, "Failed to copy asset file: " + fromAssetPath, e);
			return false;
		}
	}

	private void startLogcatCapture() {
		new Thread(() -> {
			try {
				File logFile = new File(getExternalFilesDir(null), "adbcat.log");
				if (logFile.exists()) logFile.delete();
				Runtime.getRuntime().exec("logcat -f " + logFile.getAbsolutePath());
			} catch (Exception e) {
				Log.e(TAG, "Failed to start logcat capture", e);
			}
		}).start();
	}

	@Override
	public void onDestroy() {
		super.onDestroy();
		GameNotification.INSTANCE.cancel(this);
		System.exit(0);
	}

	@Override
	protected String[] getLibraries() {
		return new String[]{"SDL2", "xash"};
	}

	@SuppressLint("HardwareIds")
	private String getAndroidID() {
		return Secure.getString(getContentResolver(), Secure.ANDROID_ID);
	}

	@SuppressLint("ApplySharedPref")
	private void saveAndroidID(String id) {
		getSharedPreferences("xash_preferences", MODE_PRIVATE).edit().putString("xash_id", id).commit();
	}

	private String loadAndroidID() {
		return getSharedPreferences("xash_preferences", MODE_PRIVATE).getString("xash_id", "");
	}

	@Override
	public String getCallingPackage() {
		if (mPackageName != null) {
			return mPackageName;
		}

		return super.getCallingPackage();
	}

	private AssetManager getAssets(boolean isEngine) {
		AssetManager am = null;

		if (isEngine) {
			am = getAssets();
		} else {
			String packageName = getCallingPackage();
			if (packageName == null || packageName.isEmpty()) {
				packageName = getPackageName();
			}
			try {
				am = getPackageManager().getResourcesForApplication(packageName).getAssets();
			} catch (Exception e) {
				Log.e(TAG, "Unable to load mod assets for package: " + packageName + ", falling back to app assets");
				e.printStackTrace();
				am = getAssets();
			}
		}

		return am;
	}

	private String[] getAssetsList(boolean isEngine, String path) {
		AssetManager am = getAssets(isEngine);

		try {
			return am.list(path);
		} catch (Exception e) {
			e.printStackTrace();
		}

		return new String[]{};
	}

	@Override
	public boolean dispatchKeyEvent(KeyEvent event) {
		if (SDLActivity.mBrokenLibraries) {
			return false;
		}

		int keyCode = event.getKeyCode();
		if (!mUseVolumeKeys) {
			if (keyCode == KeyEvent.KEYCODE_VOLUME_DOWN || keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_CAMERA || keyCode == KeyEvent.KEYCODE_ZOOM_IN || keyCode == KeyEvent.KEYCODE_ZOOM_OUT) {
				return false;
			}
		}

		return getWindow().superDispatchKeyEvent(event);
	}

	@Override
	protected String[] getArguments() {
		String gamedir = getIntent().getStringExtra("gamedir");
		if (gamedir == null || gamedir.isEmpty()) {
			if ("com.cspb.blankout".equals(getPackageName()))
				gamedir = "cspb";
			else
				gamedir = "valve";
		}
		nativeSetenv("XASH3D_GAME", gamedir);

		String gamelibdir = getIntent().getStringExtra("gamelibdir");
		if (gamelibdir != null && !gamelibdir.isEmpty()) {
			nativeSetenv("XASH3D_GAMELIBDIR", gamelibdir);
		}

		String pakfile = getIntent().getStringExtra("pakfile");
		if (pakfile != null && !pakfile.isEmpty()) {
			nativeSetenv("XASH3D_EXTRAS_PAK2", pakfile);
		}

		String basedir = getIntent().getStringExtra("basedir");
		if (basedir != null && !basedir.isEmpty()) {
			nativeSetenv("XASH3D_BASEDIR", basedir);
		} else {
			File externalFiles = getExternalFilesDir(null);
			if (externalFiles != null && new File(externalFiles, "cspb").exists()) {
				nativeSetenv("XASH3D_BASEDIR", externalFiles.getAbsolutePath());
			} else {
				nativeSetenv("XASH3D_BASEDIR",
					Environment.getExternalStorageDirectory().getAbsolutePath() + "/xash");
			}
		}

		mUseVolumeKeys = getIntent().getBooleanExtra("usevolume", false);
		mPackageName = getIntent().getStringExtra("package");

		String[] env = getIntent().getStringArrayExtra("env");
		if (env != null) {
			for (int i = 0; i + 1 < env.length; i += 2) {
				nativeSetenv(env[i], env[i + 1]);
			}
		}

		String argv = getIntent().getStringExtra("argv");
		if (argv == null || argv.trim().isEmpty()) {
			if ("com.cspb.blankout".equals(getPackageName()))
				argv = "-log";
			else argv = "-console -log";
		}

		return argv.trim().split("\\s+");
	}
}
