package app.czrwatchair

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.lifecycle.lifecycleScope
import app.czrwatchair.alert.Alerter
import app.czrwatchair.radio.RadioPermissions
import app.czrwatchair.ui.FieldwatchRoot
import app.czrwatchair.ui.FieldwatchViewModel
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private val vm: FieldwatchViewModel by viewModels()

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions(),
    ) {
        vm.refreshPermissions()
        if (RadioPermissions.granted(this)) {
            (application as FieldwatchApp).refreshFix()
            vm.startScan()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FieldwatchRoot(vm) {
                permissionLauncher.launch(RadioPermissions.required())
            }
        }
        if (RadioPermissions.granted(this)) {
            lifecycleScope.launch { vm.startScan() }
        }
        intent?.getStringExtra(Alerter.EXTRA_DEVICE_KEY)?.let { vm.select(it) }
    }

    override fun onResume() {
        super.onResume()
        vm.refreshPermissions()
        if (RadioPermissions.granted(this) && !(application as FieldwatchApp).devices.stats.value.scanning) {
            vm.startScan()
        }
    }

    override fun onNewIntent(intent: android.content.Intent) {
        super.onNewIntent(intent)
        intent.getStringExtra(Alerter.EXTRA_DEVICE_KEY)?.let { vm.select(it) }
    }
}
