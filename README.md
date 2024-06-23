# STMT
Many RGBT tracking researches primarily focus on modal fusion design, while overlooking the effective handling of target appearance changes. While some approaches have introduced historical frames or fuse and replace initial templates to incorporate temporal information, they have the risk of disrupting the original target appearance and accumulating errors over time. To alleviate these limitations, we propose a novel Transformer RGBT tracking approach, which mixes spatio-temporal multimodal tokens from the static multimodal templates and multimodal search regions in Transformer to handle target appearance changes, for robust RGBT tracking. We introduce independent dynamic template tokens to interact with the search region, embedding temporal information to address appearance changes, while also retaining the involvement of the initial static template tokens in the joint feature extraction process to ensure the preservation of the original reliable target appearance information that prevent deviations from the target appearance caused by traditional temporal updates. We also use attention mechanisms to enhance the target features of multimodal template tokens by incorporating supplementary modal cues, and make the multimodal search region tokens interact with multimodal dynamic template tokens via attention mechanisms, which facilitates the conveyance of multimodal-enhanced target change information. Our module is inserted into the transformer backbone network and inherits joint feature extraction, search-template matching, and cross-modal interaction. Extensive experiments on three RGBT benchmark datasets show that the proposed approach maintains competitive performance compared to other state-of-the-art tracking algorithms while running at 39.1 FPS. 

## News :sparkles: 

<div style="width: 100%; height: 600px;">
<canvas id="pdf-overall" style="border: 1px solid;"></canvas>
</div>
<div style="width: 100%; height: 600px;">
<canvas id="pdf-result" style="border: 1px solid;"></canvas>
</div>

<script>
var overall = 'https://github.com/YINGHAIDADA/STMT/raw/main/doc/pic/overall2-Roma-SimpleColor.pdf';
var stmt = 'https://github.com/YINGHAIDADA/STMT/raw/main/doc/pic/fig-stmt-SimpleColor.pdf';
var result = 'https://github.com/YINGHAIDADA/STMT/raw/main/doc/pic/tracker_result-2.pdf';

// 使用pdf.js渲染和显示PDF
pdfjsLib.getDocument(overall).promise.then(function(pdfDoc) {
 var canvas = document.getElementById('pdf-overall');
 var context = canvas.getContext('2d');

 // 获取PDF的第一页
 pdfDoc.getPage(1).then(function(page) {
   var viewport = page.getViewport({scale: 1});
   canvas.height = viewport.height;
   canvas.width = viewport.width;

   // 渲染PDF页面到canvas
   page.render({canvasContext: context, viewport: viewport});
 });
});

pdfjsLib.getDocument(result).promise.then(function(pdfDoc) {
 var canvas = document.getElementById('pdf-result');
 var context = canvas.getContext('2d');

 // 获取PDF的第一页
 pdfDoc.getPage(1).then(function(page) {
   var viewport = page.getViewport({scale: 1});
   canvas.height = viewport.height;
   canvas.width = viewport.width;

   // 渲染PDF页面到canvas
   page.render({canvasContext: context, viewport: viewport});
 });
});
</script>

<script src="https://mozilla.github.io/pdf.js/build/pdf.js"></script>