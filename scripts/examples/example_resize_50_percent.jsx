// 示例 JSX 脚本：将图像缩小到 50%
// 支持自动模式 - 无需确认对话框

// ===== 参数读取系统 =====
function readScriptArgs() {
    var defaultArgs = {
        auto_mode: false,
        skip_confirmation: false,
        verbose: false,
        batch_mode: false
    };

    try {
        if (typeof $.ext !== 'undefined' && $.ext.length > 0) {
            var argsFilePath = $.ext[0];
            if (argsFilePath && argsFilePath.length > 0) {
                var file = new File(argsFilePath);
                if (file.exists) {
                    file.open("r");
                    var content = file.read();
                    file.close();
                    var args = eval("(" + content + ")");
                    if (args && typeof args === 'object') {
                        if (args.verbose) {
                            $.writeln("✓ 自动模式已启用");
                        }
                        return args;
                    }
                }
            }
        }
    } catch (e) {
        $.writeln("⚠ 参数读取失败: " + e.message);
    }
    return defaultArgs;
}

// 便捷函数
function logMessage(message, level) {
    var args = readScriptArgs();
    if (args.verbose || level === "error") {
        var prefix = level === "error" ? "❌ " : level === "success" ? "✅ " : "ℹ ";
        $.writeln(prefix + message);
    }
}

function autoConfirm(message, defaultResult) {
    var args = readScriptArgs();
    if (args.skip_confirmation || args.auto_mode) {
        logMessage("自动确认: " + message, "info");
        return defaultResult;
    } else {
        return confirm(message);
    }
}

// ===== 主逻辑 =====
try {
    var args = readScriptArgs();

    // 检查是否有打开的文档
    if (app.documents.length > 0) {
        var doc = app.activeDocument;

        // 记录原始尺寸
        var originalWidth = doc.width;
        var originalHeight = doc.height;

        // 计算新尺寸（50%）
        var newWidth = originalWidth * 0.5;
        var newHeight = originalHeight * 0.5;

        // 自动确认或手动确认
        var confirmMsg = "确定要将 '" + doc.name + "' 缩小到 50% 吗？\n" +
                        "原始尺寸: " + Math.round(originalWidth) + "x" + Math.round(originalHeight) + "\n" +
                        "新尺寸: " + Math.round(newWidth) + "x" + Math.round(newHeight);

        if (autoConfirm(confirmMsg, true)) {
            // 调整图像大小
            doc.resizeImage(newWidth, newHeight, 72, ResampleMethod.BICUBIC);

            logMessage("已将 " + doc.name + " 从 " +
                      Math.round(originalWidth) + "x" + Math.round(originalHeight) +
                      " 缩小到 " +
                      Math.round(newWidth) + "x" + Math.round(newHeight), "success");

            // 保存更改
            doc.save();
            logMessage("保存完成: " + doc.name, "success");
        } else {
            logMessage("用户取消操作", "warning");
            return;
        }

    } else {
        logMessage("错误：没有打开的文档", "error");
        throw new Error("没有打开的文档");
    }
} catch (e) {
    logMessage("脚本执行出错: " + e.message, "error");
    throw e;
}
