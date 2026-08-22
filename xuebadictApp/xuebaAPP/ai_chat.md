# Flutter AI聊天页面重构方案

## 架构概览

```
lib/
├── models/
│   └── chat_message.dart              # 消息模型
├── services/
│   ├── ai_service.dart                # AI服务（已有）
│   ├── recorder_service.dart          # 录音服务（已有）
│   └── chat_session_service.dart      # 会话管理服务
├── providers/
│   └── chat_provider.dart             # 状态管理
├── pages/
│   └── ai_chat_page.dart              # 页面（纯UI）
├── widgets/
│   ├── chat_message_bubble.dart       # 消息气泡组件
│   ├── chat_input_bar.dart            # 输入栏组件
│   ├── voice_record_button.dart       # 录音按钮组件
│   └── chat_loading_indicator.dart    # 加载指示器
└── config/
    └── chat_config.dart               # 聊天配置
```

---

## 1. 消息模型 `models/chat_message.dart`

```dart
import 'package:flutter/foundation.dart';

/// 消息角色枚举
enum MessageRole { user, assistant, system }

/// 消息状态枚举
enum MessageStatus { sending, sent, error }

/// 聊天消息模型（不可变）
@immutable
class ChatMessage {
  final String id;
  final String text;
  final MessageRole role;
  final DateTime timestamp;
  final MessageStatus status;
  final String? provider;
  final String? errorDetail;

  const ChatMessage({
    required this.id,
    required this.text,
    required this.role,
    required this.timestamp,
    this.status = MessageStatus.sent,
    this.provider,
    this.errorDetail,
  });

  bool get isUser => role == MessageRole.user;
  bool get isError => status == MessageStatus.error;

  /// 创建用户消息
  factory ChatMessage.user(String text) => ChatMessage(
        id: _generateId(),
        text: text,
        role: MessageRole.user,
        timestamp: DateTime.now(),
        status: MessageStatus.sent,
      );

  /// 创建AI回复消息
  factory ChatMessage.assistant(String text, {String? provider}) => ChatMessage(
        id: _generateId(),
        text: text,
        role: MessageRole.assistant,
        timestamp: DateTime.now(),
        status: MessageStatus.sent,
        provider: provider,
      );

  /// 创建错误消息
  factory ChatMessage.error(String text, {String? detail}) => ChatMessage(
        id: _generateId(),
        text: text,
        role: MessageRole.assistant,
        timestamp: DateTime.now(),
        status: MessageStatus.error,
        errorDetail: detail,
      );

  /// 复制并修改
  ChatMessage copyWith({
    String? text,
    MessageStatus? status,
    String? errorDetail,
  }) {
    return ChatMessage(
      id: id,
      text: text ?? this.text,
      role: role,
      timestamp: timestamp,
      status: status ?? this.status,
      provider: provider,
      errorDetail: errorDetail ?? this.errorDetail,
    );
  }

  /// 转换为API格式
  Map<String, String> toApiFormat() => {
        'role': role == MessageRole.user ? 'user' : 'assistant',
        'content': text,
      };

  static String _generateId() =>
      '${DateTime.now().millisecondsSinceEpoch}_${identityHashCode(Object())}';
}
```

---

## 2. 聊天配置 `config/chat_config.dart`

```dart
/// 聊天类型枚举
enum ChatType {
  general,
  speaking,
  grammar,
  writing,
  translate,
  qa,
  planning,
  vocabulary,
}

/// 聊天配置 — 集中管理各类型的欢迎语和默认参数
class ChatConfig {
  static const Map<ChatType, String> welcomeMessages = {
    ChatType.general: '你好！我是Luna老师，有什么可以帮你的吗？可以用中文或英文和我交流哦~',
    ChatType.speaking:
        'Hi! Let\'s practice English speaking! You can talk to me in English, and I\'ll help you improve. 😊',
    ChatType.grammar: '你好！我会帮你解答任何语法问题，也可以帮你检查句子的语法是否正确。',
    ChatType.writing: '你好！我可以帮你写英语作文，或者修改你的作文。告诉我作文题目或发送你的作文吧~',
    ChatType.translate: '你好！我可以帮你翻译中英文。直接发送需要翻译的内容即可！',
    ChatType.qa: '你好！我是你的百科小助手，有任何问题都可以问我~',
    ChatType.planning: '你好！我可以帮你制定学习计划，提供学习建议。告诉我你的学习目标吧！',
    ChatType.vocabulary: '你好！我可以帮你拓展词汇，学习同义词、反义词、词组搭配等。',
  };

  /// 从字符串解析聊天类型
  static ChatType fromString(String type) {
    return ChatType.values.firstWhere(
      (e) => e.name == type,
      orElse: () => ChatType.general,
    );
  }

  /// 获取欢迎消息
  static String getWelcomeMessage(ChatType type) {
    return welcomeMessages[type] ?? '你好！有什么可以帮你的吗？';
  }

  /// AI参数配置
  static const double defaultTemperature = 0.7;
  static const int defaultMaxTokens = 2000;
}
```

---

## 3. 状态管理 `providers/chat_provider.dart`

```dart
import 'package:flutter/material.dart';
import '../models/chat_message.dart';
import '../config/chat_config.dart';
import '../services/ai_service.dart';
import '../services/recorder_service.dart';

/// 录音状态枚举
enum VoiceState { idle, recording, recognizing }

/// 聊天状态管理（ChangeNotifier）
///
/// 职责：
/// - 管理消息列表
/// - 管理加载/录音状态
/// - 协调AI服务与录音服务
class ChatProvider extends ChangeNotifier {
  final ChatType chatType;
  final String systemPrompt;
  final String? provider;

  ChatProvider({
    required this.chatType,
    required this.systemPrompt,
    this.provider,
  }) {
    _addWelcomeMessage();
  }

  // ==================== 状态字段 ====================
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;
  VoiceState _voiceState = VoiceState.idle;
  String _inputText = '';

  // ==================== Getters ====================
  List<ChatMessage> get messages => List.unmodifiable(_messages);
  bool get isLoading => _isLoading;
  VoiceState get voiceState => _voiceState;
  String get inputText => _inputText;
  bool get canSend => _inputText.trim().isNotEmpty && !_isLoading;

  // ==================== 输入管理 ====================
  void updateInputText(String text) {
    _inputText = text;
    notifyListeners();
  }

  // ==================== 消息管理 ====================
  void _addWelcomeMessage() {
    final welcomeText = ChatConfig.getWelcomeMessage(chatType);
    _messages.add(ChatMessage.assistant(welcomeText));
  }

  /// 发送消息
  Future<void> sendMessage(String text) async {
    final trimmedText = text.trim();
    if (trimmedText.isEmpty || _isLoading) return;

    // 添加用户消息
    _messages.add(ChatMessage.user(trimmedText));
    _inputText = '';
    _isLoading = true;
    notifyListeners();

    try {
      // 构建对话历史（跳过欢迎消息）
      final conversationHistory = _messages
          .skip(1)
          .map((msg) => msg.toApiFormat())
          .toList();

      // 调用AI服务
      final response = await AIService.chat(
        message: trimmedText,
        provider: provider,
        systemPrompt: systemPrompt,
        conversationHistory: conversationHistory,
        temperature: ChatConfig.defaultTemperature,
        maxTokens: ChatConfig.defaultMaxTokens,
      );

      if (response.success && response.content != null) {
        _messages.add(ChatMessage.assistant(
          response.content!,
          provider: response.provider,
        ));
      } else {
        _messages.add(ChatMessage.error(
          '抱歉，出现了一些问题。请稍后再试。',
          detail: response.error ?? '未知错误',
        ));
      }
    } catch (e) {
      _messages.add(ChatMessage.error(
        '抱歉，出现了一些问题。请稍后再试。',
        detail: e.toString(),
      ));
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// 清空对话
  void clearChat() {
    _messages.clear();
    _addWelcomeMessage();
    notifyListeners();
  }

  // ==================== 语音录制 ====================

  /// 开始录音
  Future<bool> startRecording() async {
    final success = await RecorderService.start();
    if (success) {
      _voiceState = VoiceState.recording;
      notifyListeners();
    }
    return success;
  }

  /// 停止录音并识别
  Future<String?> stopRecordingAndRecognize() async {
    if (_voiceState != VoiceState.recording) return null;

    _voiceState = VoiceState.recognizing;
    notifyListeners();

    try {
      final audioPath = await RecorderService.stop();
      if (audioPath == null) return null;

      final recognizedText = await AIService.speechToText(audioPath);
      return recognizedText;
    } finally {
      _voiceState = VoiceState.idle;
      notifyListeners();
    }
  }

  /// 取消录音
  Future<void> cancelRecording() async {
    if (_voiceState == VoiceState.recording) {
      await RecorderService.stop();
      _voiceState = VoiceState.idle;
      notifyListeners();
    }
  }

  @override
  void dispose() {
    RecorderService.dispose();
    super.dispose();
  }
}
```

---

## 4. 消息气泡组件 `widgets/chat_message_bubble.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/chat_message.dart';

/// 消息气泡组件
/// 
/// 纯展示组件，无业务逻辑
class ChatMessageBubble extends StatelessWidget {
  final ChatMessage message;
  final VoidCallback? onRetry;

  const ChatMessageBubble({
    super.key,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment:
            message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            _buildAvatar(
              icon: Icons.smart_toy,
              backgroundColor: const Color(0xFF00C897).withOpacity(0.1),
              iconColor: const Color(0xFF00C897),
            ),
            const SizedBox(width: 8),
          ],
          _buildBubbleContent(context),
          if (message.isUser) ...[
            const SizedBox(width: 8),
            _buildAvatar(
              icon: Icons.person,
              backgroundColor: Colors.blue.shade100,
              iconColor: Colors.blue.shade700,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildAvatar({
    required IconData icon,
    required Color backgroundColor,
    required Color iconColor,
  }) {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        color: backgroundColor,
        shape: BoxShape.circle,
      ),
      child: Icon(icon, color: iconColor, size: 20),
    );
  }

  Widget _buildBubbleContent(BuildContext context) {
    return Flexible(
      child: GestureDetector(
        onLongPress: () => _copyToClipboard(context),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: _getBubbleColor(),
            borderRadius: BorderRadius.only(
              topLeft: const Radius.circular(16),
              topRight: const Radius.circular(16),
              bottomLeft: Radius.circular(message.isUser ? 16 : 4),
              bottomRight: Radius.circular(message.isUser ? 4 : 16),
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.05),
                blurRadius: 8,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // 消息正文
              SelectableText(
                message.text,
                style: TextStyle(
                  color: _getTextColor(),
                  fontSize: 15,
                  height: 1.4,
                ),
              ),
              // 错误详情 + 重试
              if (message.isError && message.errorDetail != null) ...[
                const SizedBox(height: 4),
                Text(
                  '错误：${message.errorDetail}',
                  style: TextStyle(
                    color: Colors.red.shade400,
                    fontSize: 12,
                  ),
                ),
              ],
              if (message.isError && onRetry != null) ...[
                const SizedBox(height: 8),
                GestureDetector(
                  onTap: onRetry,
                  child: Text(
                    '点击重试',
                    style: TextStyle(
                      color: Colors.blue.shade600,
                      fontSize: 13,
                      decoration: TextDecoration.underline,
                    ),
                  ),
                ),
              ],
              // 时间戳
              const SizedBox(height: 4),
              Text(
                _formatTime(message.timestamp),
                style: TextStyle(
                  color: message.isUser
                      ? Colors.white.withOpacity(0.7)
                      : Colors.grey.shade500,
                  fontSize: 11,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getBubbleColor() {
    if (message.isUser) return const Color(0xFF00C897);
    if (message.isError) return Colors.red.shade50;
    return Colors.white;
  }

  Color _getTextColor() {
    if (message.isUser) return Colors.white;
    if (message.isError) return Colors.red.shade700;
    return Colors.black87;
  }

  void _copyToClipboard(BuildContext context) {
    Clipboard.setData(ClipboardData(text: message.text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('已复制到剪贴板'),
        duration: Duration(seconds: 1),
      ),
    );
  }

  String _formatTime(DateTime time) {
    return '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}';
  }
}
```

---

## 5. 录音按钮组件 `widgets/voice_record_button.dart`

```dart
import 'package:flutter/material.dart';
import '../providers/chat_provider.dart';

/// 语音录制按钮
///
/// 长按开始录音，松手停止录音并识别
class VoiceRecordButton extends StatelessWidget {
  final VoiceState voiceState;
  final VoidCallback onStartRecording;
  final VoidCallback onStopRecording;

  const VoiceRecordButton({
    super.key,
    required this.voiceState,
    required this.onStartRecording,
    required this.onStopRecording,
  });

  bool get _isRecording => voiceState == VoiceState.recording;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onLongPressStart: (_) => onStartRecording(),
      onLongPressEnd: (_) => onStopRecording(),
      onLongPressCancel: onStopRecording,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        width: 44,
        height: 44,
        decoration: BoxDecoration(
          color: _isRecording
              ? const Color(0xFFFF4D4F)
              : Colors.grey.shade100,
          shape: BoxShape.circle,
          boxShadow: _isRecording
              ? [
                  BoxShadow(
                    color: const Color(0xFFFF4D4F).withOpacity(0.4),
                    blurRadius: 12,
                    spreadRadius: 2,
                  )
                ]
              : null,
        ),
        child: Icon(
          _isRecording ? Icons.mic : Icons.mic_none_rounded,
          color: _isRecording ? Colors.white : Colors.grey.shade600,
          size: 24,
        ),
      ),
    );
  }
}
```

---

## 6. 输入栏组件 `widgets/chat_input_bar.dart`

```dart
import 'package:flutter/material.dart';
import '../providers/chat_provider.dart';
import 'voice_record_button.dart';

/// 聊天输入栏
///
/// 包含：录音按钮 + 文本输入框 + 发送按钮
class ChatInputBar extends StatelessWidget {
  final TextEditingController controller;
  final bool isLoading;
  final VoiceState voiceState;
  final VoidCallback onSend;
  final VoidCallback onStartRecording;
  final VoidCallback onStopRecording;
  final ValueChanged<String> onTextChanged;

  const ChatInputBar({
    super.key,
    required this.controller,
    required this.isLoading,
    required this.voiceState,
    required this.onSend,
    required this.onStartRecording,
    required this.onStopRecording,
    required this.onTextChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        child: Row(
          children: [
            // 录音按钮
            VoiceRecordButton(
              voiceState: voiceState,
              onStartRecording: onStartRecording,
              onStopRecording: onStopRecording,
            ),
            const SizedBox(width: 8),

            // 文本输入框
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(24),
                ),
                child: TextField(
                  controller: controller,
                  decoration: InputDecoration(
                    hintText: voiceState == VoiceState.recognizing
                        ? '正在识别语音...'
                        : '输入消息...',
                    border: InputBorder.none,
                    contentPadding:
                        const EdgeInsets.symmetric(vertical: 12),
                  ),
                  maxLines: null,
                  textInputAction: TextInputAction.send,
                  onChanged: onTextChanged,
                  onSubmitted: (_) => onSend(),
                  enabled: voiceState == VoiceState.idle,
                ),
              ),
            ),
            const SizedBox(width: 8),

            // 发送按钮
            GestureDetector(
              onTap: isLoading ? null : onSend,
              child: Container(
                width: 48,
                height: 48,
                decoration: BoxDecoration(
                  color: isLoading
                      ? Colors.grey.shade300
                      : const Color(0xFF00C897),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.send_rounded,
                  color: isLoading ? Colors.grey.shade500 : Colors.white,
                  size: 22,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 7. 加载指示器 `widgets/chat_loading_indicator.dart`

```dart
import 'package:flutter/material.dart';

/// 思考中加载指示器
class ChatLoadingIndicator extends StatelessWidget {
  final String text;

  const ChatLoadingIndicator({
    super.key,
    this.text = 'Luna正在思考中...',
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          SizedBox(
            width: 20,
            height: 20,
            child: CircularProgressIndicator(
              strokeWidth: 2,
              valueColor: AlwaysStoppedAnimation<Color>(
                Colors.grey.shade400,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Text(
            text,
            style: TextStyle(
              color: Colors.grey.shade600,
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }
}
```

---

## 8. 重构后的页面 `pages/ai_chat_page.dart`

```dart
import 'package:flutter/material.dart';
import 'package:flutter_smart_dialog/flutter_smart_dialog.dart';
import 'package:provider/provider.dart';

import '../config/chat_config.dart';
import '../providers/chat_provider.dart';
import '../utils/sound_service.dart';
import '../widgets/chat_input_bar.dart';
import '../widgets/chat_loading_indicator.dart';
import '../widgets/chat_message_bubble.dart';

/// AI聊天对话页面
///
/// 纯UI层，业务逻辑全部委托给 [ChatProvider]
class AIChatPage extends StatelessWidget {
  final String chatType;
  final String title;
  final String systemPrompt;
  final String? provider;

  const AIChatPage({
    super.key,
    required this.chatType,
    required this.title,
    required this.systemPrompt,
    this.provider,
  });

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (_) => ChatProvider(
        chatType: ChatConfig.fromString(chatType),
        systemPrompt: systemPrompt,
        provider: provider,
      ),
      child: _AIChatView(title: title),
    );
  }
}

class _AIChatView extends StatefulWidget {
  final String title;

  const _AIChatView({required this.title});

  @override
  State<_AIChatView> createState() => _AIChatViewState();
}

class _AIChatViewState extends State<_AIChatView> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  /// 滚动到底部
  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  /// 发送消息
  Future<void> _handleSend() async {
    final chatProvider = context.read<ChatProvider>();
    final text = _messageController.text.trim();
    if (text.isEmpty) return;

    SoundService.playTapSound();
    _messageController.clear();
    await chatProvider.sendMessage(text);
    _scrollToBottom();
  }

  /// 开始录音
  Future<void> _handleStartRecording() async {
    final chatProvider = context.read<ChatProvider>();
    final success = await chatProvider.startRecording();
    if (success) {
      SoundService.playTapSound();
      SmartDialog.showLoading(
        msg: '正在录音...',
        maskColor: Colors.black.withOpacity(0.5),
      );
    } else {
      SmartDialog.showToast('无法启动录音，请检查权限');
    }
  }

  /// 停止录音并识别
  Future<void> _handleStopRecording() async {
    final chatProvider = context.read<ChatProvider>();
    SmartDialog.dismiss(); // 关闭录音loading

    SmartDialog.showLoading(msg: '正在识别...');
    final recognizedText = await chatProvider.stopRecordingAndRecognize();
    SmartDialog.dismiss();

    if (recognizedText != null && recognizedText.isNotEmpty) {
      _messageController.text = recognizedText;
      chatProvider.updateInputText(recognizedText);
      // 自动发送
      _handleSend();
    } else {
      SmartDialog.showToast('未识别到内容');
    }
  }

  /// 清空对话
  void _handleClearChat() {
    SoundService.playTapSound();
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('清空对话'),
        content: const Text('确定要清空所有对话记录吗？'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('取消'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(ctx);
              context.read<ChatProvider>().clearChat();
            },
            child: const Text('确定', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: AppBar(
        title: Text(widget.title),
        backgroundColor: const Color(0xFF00C897),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            onPressed: _handleClearChat,
            icon: const Icon(Icons.delete_outline),
            tooltip: '清空对话',
          ),
        ],
      ),
      body: Consumer<ChatProvider>(
        builder: (context, chatProvider, _) {
          // 消息变化时自动滚动
          WidgetsBinding.instance.addPostFrameCallback((_) {
            _scrollToBottom();
          });

          return Column(
            children: [
              // 聊天消息列表
              Expanded(
                child: ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.all(16),
                  itemCount: chatProvider.messages.length,
                  itemBuilder: (context, index) {
                    final message = chatProvider.messages[index];
                    return ChatMessageBubble(
                      message: message,
                      onRetry: message.isError
                          ? () {
                              // 重试：取最后一条用户消息重新发送
                              final lastUserMsg = chatProvider.messages
                                  .lastWhere((m) => m.isUser,
                                      orElse: () => message);
                              if (lastUserMsg.isUser) {
                                chatProvider.sendMessage(lastUserMsg.text);
                              }
                            }
                          : null,
                    );
                  },
                ),
              ),

              // 加载指示器
              if (chatProvider.isLoading) const ChatLoadingIndicator(),

              // 输入栏
              ChatInputBar(
                controller: _messageController,
                isLoading: chatProvider.isLoading,
                voiceState: chatProvider.voiceState,
                onSend: _handleSend,
                onStartRecording: _handleStartRecording,
                onStopRecording: _handleStopRecording,
                onTextChanged: (text) =>
                    chatProvider.updateInputText(text),
              ),
            ],
          );
        },
      ),
    );
  }
}
```

---

## 9. 技术要求与规范总结

```
┌─────────────────────────────────────────────────────────────────┐
│                        技术要求总览                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 架构模式                                                     │
│     • MVVM：Provider (ChangeNotifier) 管理状态                   │
│     • 页面层纯UI，不含业务逻辑                                     │
│     • 单一职责：每个类/组件只做一件事                               │
│                                                                 │
│  2. 状态管理                                                     │
│     • 使用 provider 包                                           │
│     • ChangeNotifierProvider 创建在页面级别                       │
│     • Consumer / context.read 获取状态                           │
│     • 不可变消息模型 (immutable ChatMessage)                      │
│                                                                 │
│  3. 组件化                                                       │
│     • ChatMessageBubble — 消息气泡（支持长按复制、重试）            │
│     • VoiceRecordButton — 录音按钮（动画反馈）                    │
│     • ChatInputBar — 输入栏组合组件                               │
│     • ChatLoadingIndicator — 加载状态                            │
│                                                                 │
│  4. 语音功能流程                                                  │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐ │
│     │ 长按录音  │───▶│ 停止录音  │───▶│ 语音识别  │───▶│ 自动发送 ││
│     │ (本地)   │    │ 获取音频  │    │ (后端API) │    │ 到AI聊天 ││
│     └──────────┘    └──────────┘    └──────────┘    └─────────┘ │
│                                                                 │
│  5. AI调用流程                                                    │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐                │
│     │ 用户输入  │───▶│ 构建历史  │───▶│ AIService │               │
│     │ (文字)   │    │ 对话上下文│    │ .chat()   │               │
│     └──────────┘    └──────────┘    └──────────┘                │
│                           │                │                    │
│                           ▼                ▼                    │
│                    跳过欢迎消息      支持千问/DeepSeek            │
│                    转API格式        自动切换/指定                 │
│                                                                 │
│  6. 错误处理                                                     │
│     • 网络错误 → 显示错误气泡 + 重试按钮                          │
│     • 录音权限 → Toast提示                                       │
│     • 语音识别失败 → Toast提示                                    │
│     • try-catch 包裹所有异步操作                                  │
│                                                                 │
│  7. 性能优化                                                     │
│     • ListView.builder 懒加载消息                                │
│     • Consumer 精确重建范围                                      │
│     • 不可变模型避免不必要的rebuild                                │
│     • AnimatedContainer 代替手动动画控制器                        │
│                                                                 │
│  8. 用户体验                                                     │
│     • SelectableText 支持文本选择                                │
│     • 长按复制消息                                               │
│     • 录音按钮脉冲动画/阴影反馈                                   │
│     • 发送后自动滚动到底部                                        │
│     • 语音识别后自动发送                                          │
│                                                                 │
│  9. 依赖包                                                       │
│     • provider: ^6.0.0        状态管理                           │
│     • flutter_smart_dialog     全局弹窗/Toast                    │
│     • record: ^5.0.0          音频录制                           │
│     • http/dio                 网络请求                          │
│     • permission_handler       权限管理                          │
│                                                                 │
│ 10. 代码规范                                                     │
│     • 所有公开类/方法添加文档注释 (///)                            │
│     • 常量提取到 ChatConfig                                      │
│     • 枚举替代字符串硬编码                                        │
│     • Widget 命名语义化                                          │
│     • 文件按职责分目录存放                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 核心改进对比

| 维度 | 重构前 | 重构后 |
|------|--------|--------|
| **状态管理** | `setState` 散落在各方法中 | `ChatProvider` + `Consumer` 集中管理 |
| **组件化** | 全部写在一个文件 400+ 行 | 拆分为 7 个独立文件，每个 < 120 行 |
| **消息模型** | 简单类，无工厂方法 | 不可变模型 + 工厂构造 + 状态枚举 |
| **配置管理** | switch-case 硬编码欢迎语 | `ChatConfig` 集中管理 + 枚举映射 |
| **错误处理** | 仅显示错误文本 | 错误气泡 + 详情 + 重试按钮 |
| **语音状态** | 单个 `bool _isRecording` | `VoiceState` 枚举（idle/recording/recognizing） |
| **用户体验** | 不支持复制、不支持重试 | 长按复制、错误重试、文本可选择 |
| **可测试性** | UI和逻辑耦合，无法单元测试 | Provider 可独立单元测试 |