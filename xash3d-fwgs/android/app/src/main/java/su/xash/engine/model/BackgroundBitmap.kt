package su.xash.engine.model

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Canvas
import su.xash.engine.util.TGAReader
import java.io.File
import java.io.FileInputStream
import java.util.Scanner


object BackgroundBitmap {
	private const val BACKGROUND_ROWS = 3
	private const val BACKGROUND_COLUMNS = 4
	private const val BACKGROUND_WIDTH = 800
	private const val BACKGROUND_HEIGHT = 600
	private val FALLBACK_EXTENSIONS = arrayOf(".png", ".bmp", ".jpg", ".jpeg")

	fun createBackground(file: File): Bitmap {
		val resourceFolder = File(file, "resource")
		val layoutCandidates = listOf(
			File(resourceFolder, "HD_BackgroundLoadingLayout.txt"),
			File(resourceFolder, "BackgroundLoadingLayout.txt"),
			File(resourceFolder, "HD_BackgroundLayout.txt"),
			File(resourceFolder, "BackgroundLayout.txt")
		)

		for (layout in layoutCandidates) {
			val bitmap = loadLayoutBitmap(file, layout)
			if (bitmap != null) {
				return bitmap
			}
		}

		return loadTiledFallback(resourceFolder)
	}

	private fun loadLayoutBitmap(root: File, layoutFile: File): Bitmap? {
		if (!layoutFile.exists()) {
			return null
		}

		var bitmap = Bitmap.createBitmap(BACKGROUND_WIDTH, BACKGROUND_HEIGHT, Bitmap.Config.ARGB_8888)
		var canvas = Canvas(bitmap)
		var width = BACKGROUND_WIDTH
		var height = BACKGROUND_HEIGHT
		var loadedAny = false

		FileInputStream(layoutFile).use { inputStream ->
			Scanner(inputStream).use { scanner ->
				while (scanner.hasNext()) {
					when (val str = scanner.next()) {
						"resolution" -> {
							width = scanner.nextInt()
							height = scanner.nextInt()
							bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
							canvas = Canvas(bitmap)
						}

						else -> {
							var bmpFile = root
							str.split("/").forEach { bmpFile = File(bmpFile, it) }
							//skip
							scanner.next()
							val x = scanner.nextInt()
							val y = scanner.nextInt()
							val bmp = loadBitmapWithFallback(bmpFile)
							if (bmp != null) {
								canvas.drawBitmap(bmp, x.toFloat(), y.toFloat(), null)
								loadedAny = true
							}
						}
					}
				}
			}
		}

		return if (loadedAny) bitmap else null
	}

	private fun loadTiledFallback(resourceFolder: File): Bitmap {
		var bitmap = Bitmap.createBitmap(BACKGROUND_WIDTH, BACKGROUND_HEIGHT, Bitmap.Config.ARGB_8888)
		val canvas = Canvas(bitmap)
		val dir = File(resourceFolder, "background")
		var y = 0
		var loadedAny = false

		for (i in 0 until BACKGROUND_ROWS) {
			var x = 0
			var rowHeight = 0
			for (j in 0 until BACKGROUND_COLUMNS) {
				val filename = "${BACKGROUND_WIDTH}_${i + 1}_${'a' + j}_loading.tga"
				val bmpImage = loadBitmapWithFallback(File(dir, filename))
				if (bmpImage != null) {
					canvas.drawBitmap(bmpImage, x.toFloat(), y.toFloat(), null)
					x += bmpImage.width
					rowHeight = bmpImage.height
					loadedAny = true
				}
			}
			if (rowHeight > 0) {
				y += rowHeight
			}
		}

		return if (loadedAny) bitmap else Bitmap.createBitmap(BACKGROUND_WIDTH, BACKGROUND_HEIGHT, Bitmap.Config.ARGB_8888)
	}

	private fun loadBitmapWithFallback(file: File): Bitmap? {
		if (file.exists()) {
			return loadBitmapExact(file)
		}

		val path = file.path
		val dotIndex = path.lastIndexOf('.')
		if (dotIndex == -1) {
			return null
		}

		val basePath = path.substring(0, dotIndex)
		for (ext in FALLBACK_EXTENSIONS) {
			val candidate = File(basePath + ext)
			if (candidate.exists()) {
				return loadBitmapExact(candidate)
			}
		}
		return null
	}

	private fun loadBitmapExact(file: File): Bitmap? {
		return if (file.extension.equals("tga", ignoreCase = true)) {
			loadTga(file)
		} else {
			BitmapFactory.decodeFile(file.path)
		}
	}

	private fun loadTga(file: File): Bitmap? {
		FileInputStream(file).use {
			val buffer = it.readBytes()
			val pixels = TGAReader.read(buffer, TGAReader.ARGB)

			val width = TGAReader.getWidth(buffer)
			val height = TGAReader.getHeight(buffer)

			return Bitmap.createBitmap(pixels, 0, width, width, height, Bitmap.Config.ARGB_8888)
		}
	}
}
