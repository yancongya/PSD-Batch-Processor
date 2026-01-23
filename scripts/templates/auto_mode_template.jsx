// ============================================
// PSD Batch Processor - 自动模式脚本模板
// ============================================
// 使用说明:
// 1. 将此模板复制为新的JSX脚本
// 2. 在 "主要操作" 区域添加你的处理逻辑
// 3. 脚本会自动处理确认对话框和参数
// ============================================

// ===== 参数读取系统 =====
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

                    // 解析JSON
                    var args = parseJSON(content);

                    if (args && typeof args === 'object') {
                        if (args.verbose) {
                            $.writeln("✓ 成功读取参数文件");
                            $.writeln("  自动模式: " + args.auto_mode);
                            $.writeln("  跳过确认: " + args.skip_confirmation);
                            $.writeln("  详细输出: " + args.verbose);
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

// 简单的JSON解析器（兼容Photoshop JS引擎）
function parseJSON(jsonStr) {
    try {
        // 使用 eval 解析（注意：仅用于可信的本地数据）
        return eval("(" + jsonStr + ")");
    } catch (e) {
        $.writeln("JSON解析失败: " + e.message);
        return null;
    }
}

// ===== 便捷函数 =====

// 输出消息（带级别和自动模式检测）
function logMessage(message, level) {
    var args = readScriptArgs();
    if (args.verbose || level === "error") {
        var prefix = "";
        switch(level) {
            case "success": prefix = "✅ "; break;
            case "error": prefix = "❌ "; break;
            case "warning": prefix = "⚠ "; break;
            case "info": prefix = "ℹ "; break;
            case "debug": prefix = "🔧 "; break;
            default: prefix = "  "; break;
        }
        $.writeln(prefix + message);
    }
}

// 自动确认对话框
function autoConfirm(message, defaultResult) {
    var args = readScriptArgs();

    if (args.skip_confirmation || args.auto_mode) {
        logMessage("自动确认: " + message, "info");
        return defaultResult;
    } else {
        return confirm(message);
    }
}

// 自动输入对话框
function autoPrompt(message, defaultValue) {
    var args = readScriptArgs();

    if (args.auto_mode) {
        logMessage("自动输入: " + message + " = " + defaultValue, "info");
        return defaultValue;
    } else {
        return prompt(message, defaultValue);
    }
}

// 自动警告对话框
function autoAlert(message) {
    var args = readScriptArgs();

    if (args.skip_confirmation || args.auto_mode) {
        logMessage("警告: " + message, "warning");
        return;
    } else {
        alert(message);
    }
}

// ===== 主执行逻辑 =====

try {
    // 读取参数
    var args = readScriptArgs();

    logMessage("=== PSD Batch Processor - 脚本执行开始 ===", "info");

    // 检查是否有打开的文档
    if (app.documents.length === 0) {
        logMessage("没有打开的文档", "error");
        throw new Error("没有打开的文档");
    }

    var doc = app.activeDocument;
    var originalName = doc.name;
    var originalLayers = doc.layers ? doc.layers.length : 1;

    logMessage("处理文档: " + originalName, "info");
    logMessage("图层数量: " + originalLayers, "debug");

    // ===== 主要操作区域 =====
    // 在这里添加你的自定义处理逻辑
    // 示例：压平图像

    // 确认操作（自动或手动）
    if (originalLayers > 1) {
        var confirmMsg = "确定要压平图像 '" + originalName + "' 吗？\n这将合并 " + originalLayers + " 个图层。";

        if (autoConfirm(confirmMsg, true)) {
            // 执行压平
            doc.flatten();
            logMessage("已压平图像 (合并 " + originalLayers + " 个图层)", "success");
        } else {
            logMessage("用户取消操作", "warning");
            return;
        }
    } else {
        logMessage("文档只有一个图层，无需压平", "info");
    }

    // 保存更改
    try {
        doc.save();
        logMessage("保存完成: " + originalName, "success");
    } catch (e) {
        logMessage("保存失败: " + e.message, "error");
        throw e;
    }

    logMessage("=== 脚本执行完成 ===", "success");

} catch (e) {
    logMessage("脚本执行出错: " + e.message, "error");
    throw e; // 抛出异常，让主程序知道执行失败
}