import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_smart_dialog/flutter_smart_dialog.dart';
import 'pages/onboarding_page.dart';
import 'pages/home_page.dart';
import 'pages/settings_page.dart';
import 'pages/enhanced_word_review_page.dart';
import 'pages/algorithm_settings_page.dart';
import 'pages/login_page.dart';
import 'pages/register_page.dart';
import 'pages/invite_page.dart';
import 'pages/membership_page.dart';
import 'pages/checkin_page.dart';
import 'pages/profile_page.dart';
import 'pages/privacy_policy_page.dart';
import 'pages/grade_select_page.dart';
import 'pages/feedback_page.dart';
import 'utils/app_theme.dart';
import 'utils/learning_data_service.dart';
import 'utils/settings_helper.dart';
import 'utils/deepseek_api_service.dart';
import 'utils/auth_guard.dart';
import 'pages/library_page.dart';
import 'utils/algorithm_manager.dart';
import 'utils/auto_update_service.dart';
import 'utils/performance_optimizer.dart';
import 'utils/render_compatibility_helper.dart';
import 'services/auth_service.dart';

import 'package:provider/provider.dart';
import 'pages/home/controllers/home_controller.dart';
import 'pages/home/controllers/word_learning_controller.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // 强制初始化渲染兼容性设置，彻底解决GPU渲染问题
  await RenderCompatibilityHelper.initialize();
  
  // 强制清理所有可能的渲染缓存
  // 确保应用以最干净的状态启动
  try {
    // 多次强制清理，确保彻底
    for (int i = 0; i < 3; i++) {
      PaintingBinding.instance.imageCache.clear();
      PaintingBinding.instance.imageCache.clearLiveImages();
      await Future.delayed(const Duration(milliseconds: 100));
    }
  } catch (e) {
    // 忽略清理错误
  }

  // 优化渲染性能，解决特定设备滑动闪烁问题
  SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
  
  // 立即设置默认的系统UI覆盖层（浅色模式）
  AppTheme.setLightSystemUIOverlay();
  
  // 初始化认证服务
  await AuthService.instance.initialize();
  
  // 初始化学习数据服务
  await LearningDataService.instance.initialize();
  
  // 初始化自动更新服务
  await AutoUpdateService.instance.initialize();
  
  // 检查API Key和学习模式的兼容性
  await _validateLearningModeAndApiKey();
  
  // 延迟预热性能优化器对象池到首帧后，减少启动卡顿
  WidgetsBinding.instance.addPostFrameCallback((_) {
    PerformanceOptimizer.preWarmPools();
  });
  
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => HomeController()),
        ChangeNotifierProvider(create: (_) => WordLearningController()),
      ],
      child: const XueBaApp(),
    ),
  );
}

/// 验证学习模式和API Key的兼容性
Future<void> _validateLearningModeAndApiKey() async {
    final learningMode = await SettingsHelper.getLearningMode();
    if (learningMode == LearningMode.deepLearning) {
      final apiKey = await DeepSeekApiService.getApiKey();
      final isApiKeyValid = apiKey != null && apiKey.isNotEmpty && apiKey.length >= 10;
      
      if (!isApiKeyValid) {
        // API Key无效，自动切换到快速学习模式
        await SettingsHelper.setLearningMode(LearningMode.quickMemory);
      }
    }
}

/// 猫头鹰学英语APP应用的主入口类
/// 负责应用的整体配置、主题设置和初始路由判断
class XueBaApp extends StatefulWidget {
  const XueBaApp({super.key});

  @override
  State<XueBaApp> createState() => _XueBaAppState();
}

class _XueBaAppState extends State<XueBaApp> with WidgetsBindingObserver {
  String _themeMode = 'light'; // light, dark, parchment, cream
  double _fontScale = 1.0;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _initServices();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    AutoUpdateService.instance.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    super.didChangeAppLifecycleState(state);
    
    // 当应用从后台恢复到前台时检查更新
    if (state == AppLifecycleState.resumed) {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        if (mounted) {
          AutoUpdateService.instance.checkOnAppResume(context);
        }
      });
    }
  }

  /// 初始化所有服务
  Future<void> _initServices() async {
      // 加载主题偏好
      _loadThemePreference();
      
      // 加载字体缩放偏好
      _loadFontScalePreference();
      
      // 初始化算法管理器（LearningDataService 已在 main() 中初始化）
      await AlgorithmManager.instance.initialize();
  }

  /// 加载字体缩放偏好设置
  void _loadFontScalePreference() async {
    final fontScale = await SettingsHelper.getFontScale();
    if (_fontScale != fontScale) {
      setState(() {
        _fontScale = fontScale;
      });
    }
  }

  /// 加载主题偏好设置
  void _loadThemePreference() async {
    final prefs = await SharedPreferences.getInstance();
    final themeMode = prefs.getString('theme_mode') ?? 'light';
    
    if (_themeMode != themeMode) {
      setState(() {
        _themeMode = themeMode;
      });
      
      // 设置对应的系统UI覆盖层
      if (themeMode == 'dark') {
        AppTheme.setDarkSystemUIOverlay();
      } else {
        AppTheme.setLightSystemUIOverlay();
      }
    }
  }

  /// 切换主题
  void _toggleTheme() async {
    final prefs = await SharedPreferences.getInstance();
    // 简单的切换逻辑：light -> dark -> parchment -> cream -> light
    String newTheme;
    switch (_themeMode) {
      case 'light':
        newTheme = 'dark';
        break;
      case 'dark':
        newTheme = 'parchment';
        break;
      case 'parchment':
        newTheme = 'cream';
        break;
      case 'cream':
      default:
        newTheme = 'light';
        break;
    }
    
    setState(() {
      _themeMode = newTheme;
    });
    await prefs.setString('theme_mode', newTheme);
    
    // 更新系统UI覆盖层
    if (newTheme == 'dark') {
      AppTheme.setDarkSystemUIOverlay();
    } else {
      AppTheme.setLightSystemUIOverlay();
    }
  }

  /// 更新字体缩放
  void _updateFontScale(double scale) async {
    setState(() {
      _fontScale = scale;
    });
    await SettingsHelper.setFontScale(scale);
  }

  @override
  Widget build(BuildContext context) {
    // 根据主题模式选择对应的主题
    ThemeData selectedTheme;
    ThemeMode selectedThemeMode;
    
    switch (_themeMode) {
      case 'dark':
        selectedTheme = AppTheme.darkTheme;
        selectedThemeMode = ThemeMode.dark;
        break;
      case 'parchment':
        selectedTheme = AppTheme.parchmentTheme;
        selectedThemeMode = ThemeMode.light;
        break;
      case 'cream':
        selectedTheme = AppTheme.creamTheme;
        selectedThemeMode = ThemeMode.light;
        break;
      case 'light':
      default:
        selectedTheme = AppTheme.lightTheme;
        selectedThemeMode = ThemeMode.light;
        break;
    }
    
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '猫头鹰学英语APP',
      // 使用自定义的简约主题，支持多种主题模式
      theme: selectedTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: selectedThemeMode,
      // 全局字体缩放实现
      builder: FlutterSmartDialog.init(
        builder: (context, child) {
          return MediaQuery(
            data: MediaQuery.of(context).copyWith(
              textScaler: TextScaler.linear(_fontScale),
            ),
            child: child!,
          );
        },
      ),
      navigatorObservers: [FlutterSmartDialog.observer],
      // 使用兼容性优化的滚动行为，解决GPU渲染问题
      scrollBehavior: RenderCompatibilityHelper.getCompatibleScrollBehavior(),
      // 本地化配置
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('zh', 'CN'), // 中文
        Locale('en', 'US'), // 英文
      ],
      locale: const Locale('zh', 'CN'), // 默认使用中文
      // 初始页面通过FutureBuilder动态决定
      home: const AppInitializer(),
      // 定义应用的路由配置
      routes: {
        '/onboarding': (context) => const OnboardingPage(),
        '/login': (context) => const LoginPage(),
        '/register': (context) => const RegisterPage(),
        '/grade_select': (context) => const GradeSelectPage(),
        '/privacy': (context) => const PrivacyPolicyPage(),
        '/feedback': (context) => const FeedbackPage(),
        // 需要登录的页面
        '/home': (context) => authGuard(const HomePage()),
        '/library': (context) => authGuard(const LibraryPage()),
        '/invite': (context) => authGuard(const InvitePage()),
        '/membership': (context) => authGuard(const MembershipPage()),
        '/checkin': (context) => authGuard(const CheckinPage()),
        '/settings': (context) => authGuard(
          ThemeProvider(
            toggleTheme: _toggleTheme,
            fontScale: _fontScale,
            updateFontScale: _updateFontScale,
            child: const SettingsPage(),
          ),
        ),
        '/enhanced_word_review': (context) => authGuard(const EnhancedWordReviewPage()),
        '/algorithm_settings': (context) => authGuard(const AlgorithmSettingsPage()),
        '/profile': (context) => authGuard(const ProfilePage()),
      },
    );
  }
}

/// 主题提供者，用于向设置页面传递主题切换函数
class ThemeProvider extends InheritedWidget {
  final VoidCallback toggleTheme;
  final double fontScale;
  final Function(double) updateFontScale;

  // ignore: use_super_parameters
  const ThemeProvider({
    super.key,
    required this.toggleTheme,
    required this.fontScale,
    required this.updateFontScale,
    required Widget child,
  }) : super(child: child);

  static ThemeProvider? of(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<ThemeProvider>();
  }

  @override
  bool updateShouldNotify(ThemeProvider oldWidget) {
    return toggleTheme != oldWidget.toggleTheme || 
           fontScale != oldWidget.fontScale;
  }
}

/// 应用初始化器
/// 检查用户登录状态和初始设置，决定显示哪个页面
class AppInitializer extends StatefulWidget {
  const AppInitializer({super.key});

  @override
  State<AppInitializer> createState() => _AppInitializerState();
}

class _AppInitializerState extends State<AppInitializer> {
  @override
  void initState() {
    super.initState();
    // 在应用启动后检查更新
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        AutoUpdateService.instance.checkOnAppStart(context);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<AppStartupRoute>(
      // 检查应用启动路由
      future: _determineStartupRoute(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          // 加载中显示简约的启动画面
          return const Scaffold(
            backgroundColor: Color(0xFFF5F5F5),
            body: Center(
              child: CircularProgressIndicator(
                color: Color(0xFF666666),
              ),
            ),
          );
        }
        
        // 根据路由类型决定显示的页面
        final route = snapshot.data ?? AppStartupRoute.onboarding;
        
        switch (route) {
          case AppStartupRoute.onboarding:
            return const OnboardingPage();
          case AppStartupRoute.login:
            return const LoginPage();
          case AppStartupRoute.home:
            return const HomePage();
        }
      },
    );
  }

  /// 确定应用启动路由
  /// 优先级：引导页 > 登录页 > 首页
  Future<AppStartupRoute> _determineStartupRoute() async {
    // 1. 检查是否完成引导页
    final onboardingCompleted = await _checkOnboardingStatus();
    if (!onboardingCompleted) {
      return AppStartupRoute.onboarding;
    }
    
    // 2. 检查是否已登录
    final isLoggedIn = AuthService.instance.isLoggedIn;
    if (!isLoggedIn) {
      return AppStartupRoute.login;
    }
    
    // 3. 已登录，进入首页
    return AppStartupRoute.home;
  }

  /// 检查用户是否已完成起始页配置
  /// 返回true表示已完成，false表示需要显示起始页
  Future<bool> _checkOnboardingStatus() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('onboarding_completed') ?? false;
  }
}

/// 应用启动路由枚举
enum AppStartupRoute {
  onboarding, // 引导页
  login,      // 登录页
  home,       // 首页
}
