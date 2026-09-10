import zipfile
import os

# Define project files
pubspec_content = """name: clone_index
description: "Clone Index Multi Controller App"
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  cupertino_icons: ^1.0.8

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
"""

main_content = """import 'package:flutter/material.dart';

void main() {
  runApp(const CloneIndexApp());
}

class CloneIndexApp extends StatelessWidget {
  const CloneIndexApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Clone Index',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF121212),
        primaryColor: Colors.deepPurple,
      ),
      home: const PermissionAndControlScreen(),
    );
  }
}

class PermissionAndControlScreen extends StatefulWidget {
  const PermissionAndControlScreen({super.key});

  @override
  State<PermissionAndControlScreen> createState() =>
      _PermissionAndControlScreenState();
}

class _PermissionAndControlScreenState
    extends State<PermissionAndControlScreen> {
  // App State Variables
  bool overlayPermission = false;
  bool accessibilityPermission = false;
  bool isSyncActive = false;
  int activeClones = 4;
  int masterIndex = 1;

  // Touch Log History for Sync Verification
  List<String> clickLogs = [];

  void _addLog(String msg) {
    setState(() {
      clickLogs.insert(0, msg);
      if (clickLogs.length > 8) clickLogs.removeLast();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Clone Index - Multi Controller'),
        backgroundColor: Colors.deepPurple,
        centerTitle: true,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 1. PERMISSIONS SECTION
            const Text(
              '1. Permissions Setup',
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.purpleAccent),
            ),
            const SizedBox(height: 10),
            Card(
              color: Colors.grey[900],
              child: Column(
                children: [
                  SwitchListTile(
                    title: const Text('Display Over Other Apps (Floating)'),
                    subtitle: const Text('Floating windows screen par dikhane ke liye'),
                    value: overlayPermission,
                    activeColor: Colors.purpleAccent,
                    onChanged: (val) {
                      setState(() => overlayPermission = val);
                      _addLog(val ? "Overlay Permission Granted" : "Overlay Permission Revoked");
                    },
                  ),
                  const Divider(height: 1),
                  SwitchListTile(
                    title: const Text('Accessibility Sync Engine'),
                    subtitle: const Text('Master se baki clones par click replicate karne ke liye'),
                    value: accessibilityPermission,
                    activeColor: Colors.purpleAccent,
                    onChanged: (val) {
                      setState(() => accessibilityPermission = val);
                      _addLog(val ? "Accessibility Granted" : "Accessibility Revoked");
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // 2. CLONE CONFIGURATION SECTION
            const Text(
              '2. Clone & Sync Configuration',
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.purpleAccent),
            ),
            const SizedBox(height: 10),
            Card(
              color: Colors.grey[900],
              child: Padding(
                padding: const EdgeInsets.all(12.0),
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Active Clones Count:', style: TextStyle(fontSize: 16)),
                        DropdownButton<int>(
                          value: activeClones,
                          dropdownColor: Colors.grey[850],
                          items: [3, 4, 5].map((int val) {
                            return DropdownMenuItem<int>(
                              value: val,
                              child: Text('$val Clones'),
                            );
                          }).toList(),
                          onChanged: (val) {
                            if (val != null) setState(() => activeClones = val);
                          },
                        )
                      ],
                    ),
                    const SizedBox(height: 10),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Select Main / Master App:', style: TextStyle(fontSize: 16)),
                        DropdownButton<int>(
                          value: masterIndex,
                          dropdownColor: Colors.grey[850],
                          items: List.generate(activeClones, (i) => i + 1).map((int val) {
                            return DropdownMenuItem<int>(
                              value: val,
                              child: Text('Clone #$val'),
                            );
                          }).toList(),
                          onChanged: (val) {
                            if (val != null) {
                              setState(() => masterIndex = val);
                              _addLog("Master set to Clone #$val");
                            }
                          },
                        )
                      ],
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 20),

            // 3. FLOATING WINDOW SIMULATOR
            const Text(
              '3. Live Floating Windows & Controller',
              style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.purpleAccent),
            ),
            const SizedBox(height: 10),
            Container(
              height: 220,
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.black,
                border: Border.all(color: Colors.purpleAccent, width: 2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Master: Clone #$masterIndex',
                        style: const TextStyle(
                            color: Colors.greenAccent,
                            fontWeight: FontWeight.bold),
                      ),
                      ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(
                          backgroundColor: isSyncActive ? Colors.red : Colors.green,
                        ),
                        onPressed: () {
                          if (!overlayPermission || !accessibilityPermission) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(content: Text('Pehle dono permissions ON karein!')),
                            );
                            return;
                          }
                          setState(() => isSyncActive = !isSyncActive);
                          _addLog(isSyncActive ? "Sync Engine STARTED" : "Sync Engine STOPPED");
                        },
                        icon: Icon(isSyncActive ? Icons.stop : Icons.play_arrow),
                        label: Text(isSyncActive ? 'STOP SYNC' : 'START SYNC'),
                      )
                    ],
                  ),
                  const SizedBox(height: 10),
                  Expanded(
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      itemCount: activeClones,
                      itemBuilder: (context, index) {
                        int cloneNo = index + 1;
                        bool isMaster = (cloneNo == masterIndex);

                        return GestureDetector(
                          onTapDown: (details) {
                            if (isMaster && isSyncActive) {
                              double x = details.localPosition.dx;
                              double y = details.localPosition.dy;
                              _addLog("Master Click @ (${x.toStringAsFixed(1)}, ${y.toStringAsFixed(1)})");
                              _addLog("--> Replicated to all ${activeClones - 1} sub-clones!");
                            }
                          },
                          child: Container(
                            width: 100,
                            margin: const EdgeInsets.only(right: 8),
                            decoration: BoxDecoration(
                              color: isMaster ? Colors.purple.withOpacity(0.4) : Colors.grey[850],
                              border: Border.all(
                                color: isMaster ? Colors.greenAccent : Colors.grey,
                                width: isMaster ? 3 : 1,
                              ),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.phone_android,
                                  color: isMaster ? Colors.greenAccent : Colors.white70,
                                  size: 32,
                                ),
                                const SizedBox(height: 6),
                                Text(
                                  'Clone #$cloneNo',
                                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                                ),
                                Text(
                                  isMaster ? '(MASTER)' : '(NORMAL)',
                                  style: TextStyle(
                                    fontSize: 10,
                                    color: isMaster ? Colors.greenAccent : Colors.grey,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: 20),

            // 4. REAL-TIME EVENT LOGS
            const Text(
              '4. Live Action Console',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Container(
              height: 120,
              padding: const EdgeInsets.all(8),
              color: Colors.grey[950],
              child: ListView.builder(
                itemCount: clickLogs.length,
                itemBuilder: (context, i) => Text(
                  '> ${clickLogs[i]}',
                  style: const TextStyle(
                      fontFamily: 'monospace',
                      fontSize: 11,
                      color: Colors.greenAccent),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
"""

# Create files locally to pack into zip
os.makedirs("clone_index/lib", exist_ok=True)
with open("clone_index/pubspec.yaml", "w") as f:
    f.write(pubspec_content)

with open("clone_index/lib/main.dart", "w") as f:
    f.write(main_content)

# Zip the project
with zipfile.ZipFile("clone_index_project.zip", "w") as zipf:
    zipf.write("clone_index/pubspec.yaml", arcname="pubspec.yaml")
    zipf.write("clone_index/lib/main.dart", arcname="lib/main.dart")

print("Project generated successfully!")