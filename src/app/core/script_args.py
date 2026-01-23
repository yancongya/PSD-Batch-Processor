"""
JSX脚本参数传递系统
支持通过临时文件向Photoshop JSX脚本传递参数，实现自动模式
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import time


class ScriptArgsManager:
    """脚本参数管理器"""

    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir())
        self.args_prefix = "psd_batch_args_"

    def create_args_file(self, args: Dict[str, Any]) -> str:
        """
        创建参数文件并返回路径

        Args:
            args: 参数字典

        Returns:
            参数文件路径
        """
        # 生成唯一文件名（包含时间戳避免冲突）
        timestamp = int(time.time() * 1000)
        filename = f"{self.args_prefix}{timestamp}.json"
        args_file = self.temp_dir / filename

        # 写入参数（JSON格式）
        with open(args_file, 'w', encoding='utf-8') as f:
            json.dump(args, f, ensure_ascii=False, indent=2)

        return str(args_file)

    def create_auto_mode_args(self,
                             auto_mode: bool = True,
                             skip_confirmation: bool = True,
                             verbose: bool = True,
                             batch_mode: bool = True,
                             **extra_args) -> Dict[str, Any]:
        """
        创建自动模式参数

        Args:
            auto_mode: 自动模式开关
            skip_confirmation: 跳过确认对话框
            verbose: 详细输出
            batch_mode: 批量模式
            **extra_args: 额外参数

        Returns:
            参数字典
        """
        args = {
            "auto_mode": auto_mode,
            "skip_confirmation": skip_confirmation,
            "verbose": verbose,
            "batch_mode": batch_mode,
            "timestamp": time.time(),
            **extra_args
        }
        return args

    def cleanup_old_files(self, max_age_seconds: int = 3600):
        """
        清理旧的参数文件

        Args:
            max_age_seconds: 文件最大年龄（秒）
        """
        try:
            current_time = time.time()
            for file in self.temp_dir.glob(f"{self.args_prefix}*.json"):
                try:
                    file_age = current_time - file.stat().st_mtime
                    if file_age > max_age_seconds:
                        file.unlink()
                except:
                    pass
        except:
            pass

    def get_args_template_jsx(self) -> str:
        """
        获取JSX脚本中读取参数的模板代码

        Returns:
            JSX代码字符串
        """
        return """
// ===== PSD Batch Processor - 参数读取模板 =====
// 将此代码添加到JSX脚本开头以支持自动模式

// 读取并解析参数文件
function readScriptArgs() {
    var defaultArgs = {
        auto_mode: false,
        skip_confirmation: false,
        verbose: false,
        batch_mode: false
    };

    try {
        // 尝试从 $.ext 获取参数文件路径
        if (typeof $.ext !== 'undefined' && $.ext.length > 0) {
            var argsFilePath = $.ext[0];

            if (argsFilePath && argsFilePath.length > 0) {
                var file = new File(argsFilePath);

                if (file.exists) {
                    file.open("r");
                    var content = file.read();
                    file.close();

                    // 解析JSON（兼容Photoshop JS引擎）
                    var args = parseJSON(content);

                    if (args && typeof args === 'object') {
                        if (args.verbose) {
                            $.writeln("✓ 成功读取参数文件: " + argsFilePath);
                            $.writeln("  自动模式: " + args.auto_mode);
                            $.writeln("  跳过确认: " + args.skip_confirmation);
                        }
                        return args;
                    }
                } else if (defaultArgs.verbose) {
                    $.writeln("⚠ 参数文件不存在: " + argsFilePath);
                }
            }
        }
    } catch (e) {
        $.writeln("⚠ 读取参数失败: " + e.message);
    }

    return defaultArgs;
}

// 简单的JSON解析器（兼容Photoshop JS）
function parseJSON(jsonStr) {
    try {
        // 尝试使用 eval（注意安全风险，但仅用于本地脚本）
        return eval("(" + jsonStr + ")");
    } catch (e) {
        $.writeln("JSON解析失败: " + e.message);
        return null;
    }
}

// 获取参数（自动调用）
var scriptArgs = readScriptArgs();

// 便捷函数：是否自动模式
function isAutoMode() {
    return scriptArgs.auto_mode === true;
}

// 便捷函数：是否跳过确认
function shouldSkipConfirmation() {
    return scriptArgs.skip_confirmation === true || scriptArgs.auto_mode === true;
}

// 便捷函数：输出消息
function logMessage(message, level) {
    if (scriptArgs.verbose || level === "error") {
        var prefix = "";
        switch(level) {
            case "success": prefix = "✅ "; break;
            case "error": prefix = "❌ "; break;
            case "warning": prefix = "⚠ "; break;
            case "info": prefix = "ℹ "; break;
            default: prefix = "  "; break;
        }
        $.writeln(prefix + message);
    }
}

// 自动确认函数
function autoConfirm(message, defaultResult) {
    if (shouldSkipConfirmation()) {
        logMessage("自动确认: " + message, "info");
        return defaultResult;
    } else {
        return confirm(message);
    }
}

// ===== 模板结束 =====
"""


class AutoModeConfig:
    """自动模式配置"""

    def __init__(self):
        self.enabled = True
        self.skip_confirmation = True
        self.verbose = True
        self.batch_mode = True

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "auto_mode": self.enabled,
            "skip_confirmation": self.skip_confirmation,
            "verbose": self.verbose,
            "batch_mode": self.batch_mode,
        }

    def update(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


# 全局实例
_script_args_manager = None
_auto_mode_config = None


def get_script_args_manager() -> ScriptArgsManager:
    """获取全局参数管理器实例"""
    global _script_args_manager
    if _script_args_manager is None:
        _script_args_manager = ScriptArgsManager()
    return _script_args_manager


def get_auto_mode_config() -> AutoModeConfig:
    """获取全局自动模式配置"""
    global _auto_mode_config
    if _auto_mode_config is None:
        _auto_mode_config = AutoModeConfig()
    return _auto_mode_config


def init_auto_mode(enabled: bool = True, **kwargs):
    """初始化自动模式"""
    config = get_auto_mode_config()
    config.enabled = enabled
    config.update(**kwargs)
    return config


def save_auto_mode_config(auto_config: Dict[str, Any]):
    """
    保存自动模式配置到全局配置

    Args:
        auto_config: 自动模式配置字典
    """
    config = get_auto_mode_config()
    config.enabled = auto_config.get("enabled", False)
    config.skip_confirmation = auto_config.get("skip_confirmation", False)
    config.verbose = auto_config.get("verbose", False)
    config.batch_mode = auto_config.get("batch_mode", True)

    return config


def get_auto_mode_config_dict() -> Dict[str, Any]:
    """
    获取自动模式配置字典

    Returns:
        自动模式配置字典
    """
    config = get_auto_mode_config()
    return config.to_dict()