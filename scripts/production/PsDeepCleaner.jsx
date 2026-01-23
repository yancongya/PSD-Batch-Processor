/**
 * @author Jason
 * @email jiangran@126.com
 * @name PsDeepCleaner
 * @description photoshop metadata deep clean script (无弹窗版本)
 * @version 2.0 - Removed confirmation dialogs for batch processing
 */

// 日志输出函数
function logMessage(message, level) {
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

function deleteDocumentAncestorsMetadata() {
    if(String(app.name).search("Photoshop") > 0) {

        if(!documents.length) {
            logMessage("错误：没有打开的文档", "error");
            return;
        }

        if (ExternalObject.AdobeXMPScript == undefined) ExternalObject.AdobeXMPScript = new ExternalObject("lib:AdobeXMPScript");

        var xmp = new XMPMeta( activeDocument.xmpMetadata.rawData);
        xmp.deleteProperty(XMPConst.NS_PHOTOSHOP, "DocumentAncestors");
        app.activeDocument.xmpMetadata.rawData = xmp.serialize();

        clearDocumentAncestorsForAllLayers(app.activeDocument);

        if (app.activeDocument !== mainDocument) {
            app.activeDocument.close(SaveOptions.SAVECHANGES);
        }else{
            app.activeDocument.save();
        }
    }
}

function clearDocumentAncestorsForAllLayers(doc) {
    try {

        if (doc == undefined) {
            return;
        }

        for (var i = 0; i < doc.layers.length; i++) {
            var curLayer = doc.layers[i];
            if (curLayer.typename != "ArtLayer") {
                clearDocumentAncestorsForAllLayers(curLayer);
                continue;
            }

            if (curLayer.kind == "LayerKind.SMARTOBJECT") {

                app.activeDocument.activeLayer = curLayer;

                var idplacedLayerEditContents = stringIDToTypeID("placedLayerEditContents");
                var actionDescriptor = new ActionDescriptor();
                executeAction(idplacedLayerEditContents, actionDescriptor, DialogModes.NO);

                if(app.activeDocument.activeLayer == curLayer){
                    continue;
                }
                deleteDocumentAncestorsMetadata()
                layerSetStr += ("\n"+curLayer.name)

            }
        }
    } catch (e) {
        logMessage("图层清理失败.名称="+doc+";错误="+e, "error");
    }
}

var layerSetStr = "";
var mainDocument = app.activeDocument;

function start(){
    deleteDocumentAncestorsMetadata();
    logMessage("清理完成.\n[文档名称]:"+mainDocument.name+"\n[图层集合]:"+layerSetStr, "success");
}

try{
    // 直接执行清理，不询问用户
    start();
} catch (e) {
    logMessage("清理失败.错误="+e, "error");
}