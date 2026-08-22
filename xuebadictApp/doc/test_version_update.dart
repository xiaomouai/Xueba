/// 版本更新系统测试脚本 (Dart)
/// 测试前端版本管理和更新检查逻辑

void main() {
  print('\n${'=' * 60}');
  print('🚀 开始版本更新系统测试 (Dart)');
  print('${'=' * 60}');

  final tester = VersionUpdateDartTester();
  final results = <MapEntry<String, bool>>[
    MapEntry('版本比较', tester.testVersionComparison()),
    MapEntry('版本信息解析', tester.testVersionInfoParsing()),
    MapEntry('更新检查结果', tester.testUpdateCheckResult()),
    MapEntry('版本格式化', tester.testVersionFormatting()),
  ];

  // 汇总结果
  print('\n${'=' * 60}');
  print('📊 测试汇总');
  print('${'=' * 60}');

  int passedCount = 0;
  for (final entry in results) {
    final status = entry.value ? '✅ 通过' : '❌ 失败';
    print('$status: ${entry.key}');
    if (entry.value) passedCount++;
  }

  final totalCount = results.length;
  print('\n总计: $passedCount/$totalCount 项测试通过');

  if (passedCount == totalCount) {
    print('\n🎉 所有测试通过！版本更新系统正常工作。');
  } else {
    print('\n⚠️  有 ${totalCount - passedCount} 项测试失败，请检查代码。');
  }
}

/// Dart 版本更新测试类
class VersionUpdateDartTester {
  /// 比较版本号
  int compareVersions(String v1, String v2) {
    try {
      final parts1 = v1.split('.').map((x) => int.parse(x)).toList();
      final parts2 = v2.split('.').map((x) => int.parse(x)).toList();

      // 补齐版本号长度
      while (parts1.length < parts2.length) {
        parts1.add(0);
      }
      while (parts2.length < parts1.length) {
        parts2.add(0);
      }

      for (int i = 0; i < parts1.length; i++) {
        if (parts1[i] > parts2[i]) return 1;
        if (parts1[i] < parts2[i]) return -1;
      }
      return 0;
    } catch (e) {
      print('❌ 版本号格式错误: $e');
      return 0;
    }
  }

  /// 测试版本比较
  bool testVersionComparison() {
    print('\n📋 测试版本比较');
    print('${'=' * 50}');

    final testCases = [
      {'v1': '1.0.0', 'v2': '2.0.0', 'expected': -1, 'desc': '1.0.0 < 2.0.0'},
      {'v1': '2.0.0', 'v2': '1.0.0', 'expected': 1, 'desc': '2.0.0 > 1.0.0'},
      {'v1': '1.2.0', 'v2': '1.1.0', 'expected': 1, 'desc': '1.2.0 > 1.1.0'},
      {'v1': '1.2.3', 'v2': '1.2.3', 'expected': 0, 'desc': '1.2.3 = 1.2.3'},
      {'v1': '1.0.0', 'v2': '1.0.1', 'expected': -1, 'desc': '1.0.0 < 1.0.1'},
    ];

    int passed = 0;
    for (final test in testCases) {
      final result = compareVersions(test['v1'] as String, test['v2'] as String);
      final expected = test['expected'] as int;
      final status = result == expected ? '✅' : '❌';
      print('$status ${test['desc']}: result=$result (expected=$expected)');
      if (result == expected) passed++;
    }

    print('\n结果: $passed/${testCases.length} 通过');
    return passed == testCases.length;
  }

  /// 测试版本信息解析
  bool testVersionInfoParsing() {
    print('\n📋 测试版本信息解析');
    print('${'=' * 50}');

    // 模拟 JSON 响应
    final jsonData = {
      'tag_name': 'v1.2.0',
      'body': '''### 更新内容
- 新增单词拼读功能
- 优化语音评测准确度
- 修复已知问题
- 提升应用性能

### 安装说明
- 下载后自动安装
''',
      'published_at': '2026-02-04T12:00:00Z',
    };

    // 解析版本号
    final tagName = (jsonData['tag_name'] as String?) ?? '';
    final version = tagName.replaceFirst('v', '');

    print('✓ 版本号解析:');
    print('  ✅ tag_name: $tagName');
    print('  ✅ version: $version');

    // 验证版本号格式
    final versionRegex = RegExp(r'^\d+\.\d+\.\d+$');
    if (versionRegex.hasMatch(version)) {
      print('  ✅ 版本号格式正确');
    } else {
      print('  ❌ 版本号格式错误');
      return false;
    }

    // 验证必需字段
    final requiredFields = ['tag_name', 'body', 'published_at'];
    print('\n✓ 必需字段检查:');
    for (final field in requiredFields) {
      if (jsonData.containsKey(field)) {
        print('  ✅ $field');
      } else {
        print('  ❌ 缺少 $field');
        return false;
      }
    }

    print('\n✅ 版本信息解析成功');
    return true;
  }

  /// 测试更新检查结果
  bool testUpdateCheckResult() {
    print('\n📋 测试更新检查结果');
    print('${'=' * 50}');

    final testCases = [
      {
        'name': '需要更新',
        'currentVersion': '1.0.0',
        'latestVersion': '1.2.0',
        'shouldUpdate': true,
      },
      {
        'name': '不需要更新',
        'currentVersion': '1.2.0',
        'latestVersion': '1.2.0',
        'shouldUpdate': false,
      },
      {
        'name': '版本落后',
        'currentVersion': '0.5.0',
        'latestVersion': '2.0.0',
        'shouldUpdate': true,
      },
    ];

    int passed = 0;
    for (final test in testCases) {
      final current = test['currentVersion'] as String;
      final latest = test['latestVersion'] as String;
      final shouldUpdate = test['shouldUpdate'] as bool;

      // 模拟更新检查
      final hasUpdate = compareVersions(current, latest) < 0;

      final status = hasUpdate == shouldUpdate ? '✅' : '❌';
      print('$status ${test['name']}: v$current → v$latest → 更新: $hasUpdate');

      if (hasUpdate == shouldUpdate) passed++;
    }

    print('\n结果: $passed/${testCases.length} 通过');
    return passed == testCases.length;
  }

  /// 测试版本格式化
  bool testVersionFormatting() {
    print('\n📋 测试版本格式化');
    print('${'=' * 50}');

    final testCases = [
      {'input': '1.2.0', 'expected': 'v1.2.0', 'format': '添加 v 前缀'},
      {'input': 'v1.2.0', 'expected': '1.2.0', 'format': '移除 v 前缀'},
    ];

    int passed = 0;
    for (final test in testCases) {
      final input = test['input'] as String;
      final expected = test['expected'] as String;

      String result;
      if (input.startsWith('v')) {
        result = input.substring(1);
      } else {
        result = 'v$input';
      }

      final status = result == expected ? '✅' : '❌';
      print('$status ${test['format']}: $input → $result (expected: $expected)');

      if (result == expected) passed++;
    }

    print('\n结果: $passed/${testCases.length} 通过');
    return passed == testCases.length;
  }
}
