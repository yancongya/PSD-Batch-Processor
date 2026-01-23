// 示例 JSX 脚本：自动合并所有图层（压平图像）- 无需确认
// 这个版本自动处理所有确认，适合无人值守运行

try {
    // 检查是否有打开的文档
    if (app.documents.length > 0) {
        var doc = app.activeDocument;

        // 记录原始信息
        var originalName = doc.name;
        var originalLayers = doc.layers.length;

        // 自动确认执行（无需用户交互）
        var autoConfirm = true; // 自动模式开关

        if (autoConfirm) {
            // 自动模式：直接执行，不显示确认对话框
            if (doc.layers.length > 1) {
                doc.flatten();
                $.writeln("✅ 自动压平完成: " + originalName + " (合并 " + originalLayers + " 个图层)");
            } else {
                $.writeln("ℹ️ 文档只有一个图层，无需压平");
            }

            // 保存更改
            doc.save();
            $.writeln("💾 保存完成: " + originalName);

        } else {
            // 手动模式：显示确认对话框（原逻辑）
            var result = confirm("确定要压平图像 '" + originalName + "' 吗？\n这将合并 " + originalLayers + " 个图层。");
            if (result) {
                if (doc.layers.length > 1) {
                    doc.flatten();
                    $.writeln("已将 " + originalName + " 压平（合并 " + originalLayers + " 个图层）");
                } else {
                    $.writeln("文档只有一个图层，无需压平");
                }
                doc.save();
                $.writeln("保存完成");
            } else {
                $.writeln("用户取消操作");
            }
        }

    } else {
        $.writeln("❌ 错误：没有打开的文档");
        throw new Error("没有打开的文档");
    }
} catch (e) {
    $.writeln("❌ 脚本执行出错: " + e.message);
    throw e; // 抛出异常，让主程序知道执行失败
}