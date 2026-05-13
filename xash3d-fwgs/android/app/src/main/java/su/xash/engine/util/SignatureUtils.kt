package su.xash.engine.util

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import java.security.MessageDigest

object SignatureUtils {
    fun getApkSigningCertSha256(context: Context): ByteArray {
        val pm = context.packageManager
        val pkg = context.packageName

        val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            val pkgInfo = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                pm.getPackageInfo(
                    pkg,
                    PackageManager.PackageInfoFlags.of(PackageManager.GET_SIGNING_CERTIFICATES.toLong())
                )
            } else {
                @Suppress("DEPRECATION")
                pm.getPackageInfo(pkg, PackageManager.GET_SIGNING_CERTIFICATES)
            }

            val signing = pkgInfo.signingInfo
            val arr = signing.apkContentsSigners
            if (arr.isNullOrEmpty()) {
                throw IllegalStateException("No APK signatures found")
            }
            arr[0].toByteArray()
        } else {
            @Suppress("DEPRECATION")
            val pkgInfo = pm.getPackageInfo(pkg, PackageManager.GET_SIGNATURES)
            @Suppress("DEPRECATION")
            val arr = pkgInfo.signatures
            if (arr.isNullOrEmpty()) {
                throw IllegalStateException("No APK signatures found")
            }
            @Suppress("DEPRECATION")
            arr[0].toByteArray()
        }

        val md = MessageDigest.getInstance("SHA-256")
        return md.digest(signatures)
    }

    fun toHexLower(bytes: ByteArray): String {
        val out = StringBuilder(bytes.size * 2)
        for (b in bytes) {
            out.append("0123456789abcdef"[(b.toInt() ushr 4) and 0xF])
            out.append("0123456789abcdef"[b.toInt() and 0xF])
        }
        return out.toString()
    }
}
