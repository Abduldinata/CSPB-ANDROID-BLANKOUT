package su.xash.engine.ui.credits

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import su.xash.engine.R
import su.xash.engine.databinding.FragmentCreditsBinding

class CreditsFragment : Fragment() {
	private var _binding: FragmentCreditsBinding? = null
	private val binding get() = _binding!!

	override fun onCreateView(
		inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
	): View {
		_binding = FragmentCreditsBinding.inflate(inflater, container, false)
		return binding.root
	}

	override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
		super.onViewCreated(view, savedInstanceState)

		binding.toolbar.setNavigationOnClickListener {
			findNavController().navigateUp()
		}

		binding.creditsBody.text = getString(R.string.credits_body)
		binding.linkBill.setOnClickListener {
			openUrl("https://www.youtube.com/@BillFLX")
		}
		binding.linkTempo.setOnClickListener {
			openUrl("https://www.youtube.com/@TempoChannel5")
		}
		binding.linkSheesh.setOnClickListener {
			openUrl("https://www.youtube.com/@Sheesh5576")
		}
		binding.linkGithub.setOnClickListener {
			openUrl("https://github.com/FWGS/xash3d-fwgs")
		}
	}

	private fun openUrl(url: String) {
		startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
	}

	override fun onDestroyView() {
		super.onDestroyView()
		_binding = null
	}
}
