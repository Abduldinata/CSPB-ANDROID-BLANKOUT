package su.xash.engine.ui.library

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.widget.doAfterTextChanged
import androidx.core.view.isVisible
import androidx.fragment.app.Fragment
import androidx.fragment.app.activityViewModels
import androidx.navigation.fragment.findNavController
import com.google.android.material.tabs.TabLayout
import su.xash.engine.R
import su.xash.engine.databinding.FragmentLauncherCspbBinding
import su.xash.engine.model.Game

class LauncherCspbFragment : Fragment() {
	private var _binding: FragmentLauncherCspbBinding? = null
	private val binding get() = _binding!!

	private val libraryViewModel: LibraryViewModel by activityViewModels()
	private var selectedGame: Game? = null

	override fun onCreateView(
		inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
	): View {
		_binding = FragmentLauncherCspbBinding.inflate(inflater, container, false)
		return binding.root
	}

	override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
		super.onViewCreated(view, savedInstanceState)

		setupTabs()
		setupToolbarMenu()
		setupAdvancedCmdline()
		setupCopyProgressUi()

		// Load games list and pick CSPB by default.
		libraryViewModel.installedGames.observe(viewLifecycleOwner) { games ->
			if (games.isNullOrEmpty()) return@observe

			val cspb = games.firstOrNull { it.basedir.name.equals("cspb", ignoreCase = true) }
				?: games.firstOrNull()
				?: return@observe

			if (selectedGame?.basedir?.absolutePath == cspb.basedir.absolutePath) return@observe

			selectedGame = cspb
			libraryViewModel.setSelectedGame(cspb)
			bindSelectedGame(cspb)
		}
		libraryViewModel.reloadGames(requireContext())

		binding.launchButton.setOnClickListener {
			val game = selectedGame ?: return@setOnClickListener
			libraryViewModel.startEngine(requireContext(), game)
		}
	}

	private fun setupTabs() {
		// Match Bill-like UI: NORMAL / ADVANCED.
		binding.tabs.apply {
			removeAllTabs()
			addTab(newTab().setText(R.string.launcher_tab_normal))
			addTab(newTab().setText(R.string.launcher_tab_advanced))
			getTabAt(0)?.select()

			addOnTabSelectedListener(object : TabLayout.OnTabSelectedListener {
				override fun onTabSelected(tab: TabLayout.Tab) {
					val isAdvanced = tab.position == 1
					binding.normalContainer.visibility = if (isAdvanced) View.GONE else View.VISIBLE
					binding.advancedContainer.visibility = if (isAdvanced) View.VISIBLE else View.GONE
				}

				override fun onTabUnselected(tab: TabLayout.Tab) = Unit
				override fun onTabReselected(tab: TabLayout.Tab) = Unit
			})
		}
	}

	private fun setupToolbarMenu() {
		binding.toolbar.setOnMenuItemClickListener { item ->
			when (item.itemId) {
				R.id.action_credits -> {
					findNavController().navigate(R.id.creditsFragment)
					true
				}
				R.id.action_quit -> {
					requireActivity().finish()
					true
				}
				else -> false
			}
		}
	}

	private fun setupAdvancedCmdline() {
		binding.cmdlineInput.setOnFocusChangeListener { _, hasFocus ->
			if (hasFocus) return@setOnFocusChangeListener
			saveCmdline()
		}
		binding.resolutionWidthInput.doAfterTextChanged { saveCmdline() }
		binding.resolutionHeightInput.doAfterTextChanged { saveCmdline() }
		binding.soundEnabledSwitch.setOnCheckedChangeListener { _, _ -> saveCmdline() }
		binding.volumeButtonsSwitch.setOnCheckedChangeListener { _, _ -> saveCmdline() }
		binding.keyboardResizeSwitch.setOnCheckedChangeListener { _, _ -> saveCmdline() }
		binding.customResolutionSwitch.setOnCheckedChangeListener { _, _ ->
			updateResolutionEnabledState()
			saveCmdline()
		}
		binding.cmdlineSave.setOnClickListener {
			saveCmdline()
		}
	}

	private fun saveCmdline() {
		val game = selectedGame ?: return
		val args = binding.cmdlineInput.text?.toString()?.trim().orEmpty()
		val prefs = requireContext().getSharedPreferences(game.basedir.name, Context.MODE_PRIVATE)
		prefs.edit()
			.putString("arguments", if (args.isBlank()) "-console" else args)
			.putBoolean("sound_enabled", binding.soundEnabledSwitch.isChecked)
			.putBoolean("use_volume_buttons", binding.volumeButtonsSwitch.isChecked)
			.putBoolean("keyboard_resizes_screen", binding.keyboardResizeSwitch.isChecked)
			.putBoolean("use_custom_resolution", binding.customResolutionSwitch.isChecked)
			.putString("custom_width", binding.resolutionWidthInput.text?.toString()?.trim().orEmpty())
			.putString("custom_height", binding.resolutionHeightInput.text?.toString()?.trim().orEmpty())
			.apply()
	}

	private fun setupCopyProgressUi() {
		libraryViewModel.dataSyncProgress.observe(viewLifecycleOwner) { p ->
			val visible = p != null
			binding.syncOverlay.isVisible = visible
			binding.launchButton.isEnabled = !visible
			if (p != null) {
				binding.syncProgressBar.progress = p.percent
				val tail = p.current?.let { "\n$it" } ?: ""
				binding.syncProgressText.text = "${p.phase} (${p.percent}%)$tail"
			}
		}
	}

	private fun bindSelectedGame(game: Game) {
		// Use cover if available; fallback to icon.
		val bmp = game.cover ?: game.icon
		if (bmp != null) {
			binding.gameLogo.setImageBitmap(bmp)
		} else {
			binding.gameLogo.setImageResource(android.R.mipmap.sym_def_app_icon)
		}

		// Show resolved game root path (created by LibraryViewModel).
		val appPrefs = requireContext().getSharedPreferences("app_preferences", Context.MODE_PRIVATE)
		val rootPath = appPrefs.getString("game_path", game.basedir.parent ?: "") ?: ""
		binding.pathValue.text = rootPath

		// Load per-game command line args for ADVANCED tab.
		val prefs = requireContext().getSharedPreferences(game.basedir.name, Context.MODE_PRIVATE)
		val args = prefs.getString("arguments", "-console") ?: "-console"
		binding.cmdlineInput.setText(args)
		binding.soundEnabledSwitch.isChecked = prefs.getBoolean("sound_enabled", true)
		binding.volumeButtonsSwitch.isChecked = prefs.getBoolean("use_volume_buttons", false)
		binding.keyboardResizeSwitch.isChecked = prefs.getBoolean("keyboard_resizes_screen", true)
		binding.customResolutionSwitch.isChecked = prefs.getBoolean("use_custom_resolution", false)
		binding.resolutionWidthInput.setText(prefs.getString("custom_width", ""))
		binding.resolutionHeightInput.setText(prefs.getString("custom_height", ""))
		updateResolutionEnabledState()

/*
		// Advanced settings list (preferences) for this game.
		childFragmentManager.beginTransaction()
			.replace(binding.advancedPrefs.id, GameSettingsPreferenceFragment(game))
			.commitAllowingStateLoss()
*/
	}

	override fun onDestroyView() {
		super.onDestroyView()
		_binding = null
	}

	private fun updateResolutionEnabledState() {
		val enabled = binding.customResolutionSwitch.isChecked
		binding.resolutionWidthInput.isEnabled = enabled
		binding.resolutionHeightInput.isEnabled = enabled
	}
}
