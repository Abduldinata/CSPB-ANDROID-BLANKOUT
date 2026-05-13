package su.xash.engine.util

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.graphics.BitmapFactory
import android.os.Build
import androidx.core.app.NotificationCompat
import su.xash.engine.MainActivity
import su.xash.engine.R
import su.xash.engine.receiver.ExitGameReceiver

object GameNotification {
	private const val CHANNEL_ID = "game_session"
	private const val NOTIF_ID = 0x43535042 // "CSPB"
	private const val ACTION_EXIT = "su.xash.engine.action.EXIT_GAME"

	fun showGameRunning(ctx: Context) {
		val nm = ctx.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager

		if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
			val ch = NotificationChannel(
				CHANNEL_ID,
				"Game Session",
				NotificationManager.IMPORTANCE_LOW
			).apply {
				description = "CSPB session controls"
				setShowBadge(false)
			}
			nm.createNotificationChannel(ch)
		}

		val exitIntent = Intent(ctx, ExitGameReceiver::class.java).apply { action = ACTION_EXIT }
		val exitPending = PendingIntent.getBroadcast(
			ctx,
			0,
			exitIntent,
			(PendingIntent.FLAG_UPDATE_CURRENT or if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
		)

		val openIntent = Intent(ctx, MainActivity::class.java).apply {
			addFlags(Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP)
		}
		val openPending = PendingIntent.getActivity(
			ctx,
			1,
			openIntent,
			(PendingIntent.FLAG_UPDATE_CURRENT or if (Build.VERSION.SDK_INT >= 23) PendingIntent.FLAG_IMMUTABLE else 0)
		)

		val largeIcon = BitmapFactory.decodeResource(ctx.resources, R.mipmap.cspb_app_icon)

		val notif = NotificationCompat.Builder(ctx, CHANNEL_ID)
			.setSmallIcon(R.mipmap.cspb_app_icon)
			.setLargeIcon(largeIcon)
			.setContentTitle(ctx.getString(R.string.app_name))
			.setContentText("Game running")
			.setContentIntent(openPending)
			.setOngoing(true)
			.addAction(0, "Exit", exitPending)
			.build()

		nm.notify(NOTIF_ID, notif)
	}

	fun cancel(ctx: Context) {
		val nm = ctx.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
		nm.cancel(NOTIF_ID)
	}
}

