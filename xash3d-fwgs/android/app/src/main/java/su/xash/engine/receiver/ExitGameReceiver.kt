package su.xash.engine.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Process
import su.xash.engine.util.GameNotification

class ExitGameReceiver : BroadcastReceiver() {
	override fun onReceive(context: Context, intent: Intent) {
		GameNotification.cancel(context)
		Process.killProcess(Process.myPid())
	}
}

