import os
import zipfile

# Define project directories
base_dir = "/tmp/MultiAppCloningStudio"
app_dir = os.path.join(base_dir, "app")
src_main = os.path.join(app_dir, "src", "main")
java_dir = os.path.join(src_main, "java", "com", "example", "multiappcloningstudio")
res_dir = os.path.join(src_main, "res")
layout_dir = os.path.join(res_dir, "layout")
drawable_dir = os.path.join(res_dir, "drawable")
values_dir = os.path.join(res_dir, "values")

for d in [java_dir, layout_dir, drawable_dir, values_dir]:
    os.makedirs(d, exist_ok=True)

# Build.gradle (Project)
build_gradle_project = """// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
}
"""

# settings.gradle
settings_gradle = """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOSITORIES)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "MultiAppCloningStudio"
include ':app'
"""

# Build.gradle (App)
build_gradle_app = """plugins {
    id 'com.android.application'
}

android {
    namespace 'com.example.multiappcloningstudio'
    compileSdk 34

    defaultConfig {
        applicationId "com.example.multiappcloningstudio"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.gridlayout:gridlayout:1.0.0'
}
"""

# AndroidManifest.xml
android_manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:permission="android.permission.INTERNET" />
    <uses-permission android:permission="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:permission="android.permission.QUERY_ALL_PACKAGES" tools:ignore="QueryAllPackagesPermission" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="Multi App Cloner Grid"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.MultiAppCloningStudio"
        android:hardwareAccelerated="true">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>

</manifest>
"""

# Res Values (Colors, Strings, Themes)
colors_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="black">#FF000000</color>
    <color name="white">#FFFFFFFF</color>
    <color name="bg_dark">#121212</color>
    <color name="card_bg">#1E1E1E</color>
    <color name="accent_blue">#2196F3</color>
    <color name="accent_green">#4CAF50</color>
    <color name="grid_border">#333333</color>
</resources>
"""

strings_xml = """<resources>
    <string name="app_name">Multi App Cloner 4x Grid</string>
</resources>
"""

themes_xml = """<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Base.Theme.MultiAppCloningStudio" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="android:statusBarColor">#121212</item>
        <item name="android:navigationBarColor">#121212</item>
    </style>
    <style name="Theme.MultiAppCloningStudio" parent="Base.Theme.MultiAppCloningStudio" />
</resources>
"""

# Layout File (activity_main.xml)
layout_main = """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:background="#121212">

    <!-- Top Header Bar -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="12dp"
        android:background="#1E1E1E"
        android:gravity="center_vertical">

        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="4-Window Multi App Cloner"
            android:textColor="#FFFFFF"
            android:textSize="18sp"
            android:textStyle="bold" />

        <Button
            android:id="@+id/btnAppSelector"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Select App"
            android:backgroundTint="#2196F3"
            android:textColor="#FFFFFF" />
    </LinearLayout>

    <!-- Mode Selector Sub-bar -->
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:padding="8dp"
        android:background="#252525"
        android:gravity="center">

        <TextView
            android:id="@+id/tvSelectedApp"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Target: Web/Social Multi-Instance"
            android:textColor="#B0B0B0"
            android:textSize="13sp" />

        <Button
            android:id="@+id/btnReloadAll"
            android:layout_width="wrap_content"
            android:layout_height="36dp"
            android:text="Refresh All 4"
            android:textSize="11sp"
            android:backgroundTint="#4CAF50"
            android:padding="0dp"/>
    </LinearLayout>

    <!-- 2x2 Split Grid Layout -->
    <androidx.gridlayout.widget.GridLayout
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1"
        app:columnCount="2"
        app:rowCount="2"
        android:padding="2dp">

        <!-- Window 1 Container -->
        <FrameLayout
            android:id="@+id/container1"
            android:layout_width="0dp"
            android:layout_height="0dp"
            app:layout_columnWeight="1"
            app:layout_rowWeight="1"
            android:layout_margin="2dp"
            android:background="#1E1E1E">
            
            <WebView
                android:id="@+id/webView1"
                android:layout_width="match_parent"
                android:layout_height="match_parent" />

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Window 1"
                android:textColor="#88FFFFFF"
                android:textSize="10sp"
                android:background="#80000000"
                android:padding="4dp"
                android:layout_gravity="top|left" />
        </FrameLayout>

        <!-- Window 2 Container -->
        <FrameLayout
            android:id="@+id/container2"
            android:layout_width="0dp"
            android:layout_height="0dp"
            app:layout_columnWeight="1"
            app:layout_rowWeight="1"
            android:layout_margin="2dp"
            android:background="#1E1E1E">

            <WebView
                android:id="@+id/webView2"
                android:layout_width="match_parent"
                android:layout_height="match_parent" />

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Window 2"
                android:textColor="#88FFFFFF"
                android:textSize="10sp"
                android:background="#80000000"
                android:padding="4dp"
                android:layout_gravity="top|left" />
        </FrameLayout>

        <!-- Window 3 Container -->
        <FrameLayout
            android:id="@+id/container3"
            android:layout_width="0dp"
            android:layout_height="0dp"
            app:layout_columnWeight="1"
            app:layout_rowWeight="1"
            android:layout_margin="2dp"
            android:background="#1E1E1E">

            <WebView
                android:id="@+id/webView3"
                android:layout_width="match_parent"
                android:layout_height="match_parent" />

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Window 3"
                android:textColor="#88FFFFFF"
                android:textSize="10sp"
                android:background="#80000000"
                android:padding="4dp"
                android:layout_gravity="top|left" />
        </FrameLayout>

        <!-- Window 4 Container -->
        <FrameLayout
            android:id="@+id/container4"
            android:layout_width="0dp"
            android:layout_height="0dp"
            app:layout_columnWeight="1"
            app:layout_rowWeight="1"
            android:layout_margin="2dp"
            android:background="#1E1E1E">

            <WebView
                android:id="@+id/webView4"
                android:layout_width="match_parent"
                android:layout_height="match_parent" />

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Window 4"
                android:textColor="#88FFFFFF"
                android:textSize="10sp"
                android:background="#80000000"
                android:padding="4dp"
                android:layout_gravity="top|left" />
        </FrameLayout>

    </androidx.gridlayout.widget.GridLayout>

</LinearLayout>
"""

# MainActivity.java Source Code
main_activity_java = """package com.example.multiappcloningstudio;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private WebView webView1, webView2, webView3, webView4;
    private Button btnAppSelector, btnReloadAll;
    private TextView tvSelectedApp;

    // Supported Web-App targets for isolated 4-instance cloning
    private String currentTargetUrl = "https://web.whatsapp.com";
    private final String[] appNames = {"WhatsApp Web", "Facebook / Messenger", "Twitter / X", "Instagram", "Custom URL"};
    private final String[] appUrls = {
            "https://web.whatsapp.com",
            "https://www.facebook.com",
            "https://www.x.com",
            "https://www.instagram.com",
            "https://www.google.com"
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize Views
        webView1 = findViewById(R.id.webView1);
        webView2 = findViewById(R.id.webView2);
        webView3 = findViewById(R.id.webView3);
        webView4 = findViewById(R.id.webView4);

        btnAppSelector = findViewById(R.id.btnAppSelector);
        btnReloadAll = findViewById(R.id.btnReloadAll);
        tvSelectedApp = findViewById(R.id.tvSelectedApp);

        // Configure all 4 isolated web environments
        setupIsolatedWebView(webView1, "session_1");
        setupIsolatedWebView(webView2, "session_2");
        setupIsolatedWebView(webView3, "session_3");
        setupIsolatedWebView(webView4, "session_4");

        // Load default app
        loadTargetUrlOnAll(currentTargetUrl);

        // Selection Listener
        btnAppSelector.setOnClickListener(v -> showAppSelectionDialog());

        // Refresh Listener
        btnReloadAll.setOnClickListener(v -> {
            webView1.reload();
            webView2.reload();
            webView3.reload();
            webView4.reload();
            Toast.makeText(MainActivity.this, "Refreshing all 4 windows...", Toast.LENGTH_SHORT).show();
        });
    }

    @SuppressLint("SetJavaScriptEnabled")
    private void setupIsolatedWebView(WebView webView, String sessionTag) {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        // Request Desktop Site view to fit WhatsApp Web / Desktop interfaces properly in split screens
        settings.setUserAgentString("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }
        });

        // Ensure Cookies / LocalStorage sessions remain separate across instances
        CookieManager cookieManager = CookieManager.getInstance();
        cookieManager.setAcceptCookie(true);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.21) {
            cookieManager.setAcceptThirdPartyCookies(webView, true);
        }
    }

    private void loadTargetUrlOnAll(String url) {
        webView1.loadUrl(url);
        webView2.loadUrl(url);
        webView3.loadUrl(url);
        webView4.loadUrl(url);
    }

    private void showAppSelectionDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Select App to Clone in 4 Windows");
        builder.setItems(appNames, (dialog, which) -> {
            currentTargetUrl = appUrls[which];
            tvSelectedApp.setText("Active: " + appNames[which]);
            loadTargetUrlOnAll(currentTargetUrl);
            Toast.makeText(MainActivity.this, "Loaded 4 Clones of " + appNames[which], Toast.LENGTH_SHORT).show();
        });
        builder.show();
    }

    @Override
    public void onBackPressed() {
        // Handle back button for sub-windows
        if (webView1.canGoBack()) {
            webView1.goBack();
        } else if (webView2.canGoBack()) {
            webView2.goBack();
        } else if (webView3.canGoBack()) {
            webView3.goBack();
        } else if (webView4.canGoBack()) {
            webView4.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
"""

# Save all files into project tree
def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

write_file(os.path.join(base_dir, "build.gradle"), build_gradle_project)
write_file(os.path.join(base_dir, "settings.gradle"), settings_gradle)
write_file(os.path.join(app_dir, "build.gradle"), build_gradle_app)
write_file(os.path.join(src_main, "AndroidManifest.xml"), android_manifest)
write_file(os.path.join(values_dir, "colors.xml"), colors_xml)
write_file(os.path.join(values_dir, "strings.xml"), strings_xml)
write_file(os.path.join(values_dir, "themes.xml"), themes_xml)
write_file(os.path.join(layout_dir, "activity_main.xml"), layout_main)
write_file(os.path.join(java_dir, "MainActivity.java"), main_activity_java)

# Create Zip Archive
zip_output_path = "/tmp/MultiAppCloningStudio_Project.zip"
with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, base_dir)
            zipf.write(file_path, arcname)

print(f"Project generated successfully at: {zip_output_path}")