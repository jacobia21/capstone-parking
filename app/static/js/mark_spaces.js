var canvas = this.__canvas = new fabric.Canvas('c');
fabric.Image.fromURL("/static/img/lot_map.png", function (img) {    
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
        scaleX: canvas.width / img.width,
        scaleY: canvas.height / img.height
    });
});

canvas.on('object:moving', function (e) {
  var obj = e.target;
  // if object is too big ignore
  if(obj.currentHeight > obj.canvas.height || obj.currentWidth > obj.canvas.width){
    return;
  }
  obj.setCoords();
  // top-left  corner
  if(obj.getBoundingRect().top < 0 || obj.getBoundingRect().left < 0){
    obj.top = Math.max(obj.top, obj.top-obj.getBoundingRect().top);
    obj.left = Math.max(obj.left, obj.left-obj.getBoundingRect().left);
  }
  // bot-right corner
  if(obj.getBoundingRect().top+obj.getBoundingRect().height  > obj.canvas.height || obj.getBoundingRect().left+obj.getBoundingRect().width  > obj.canvas.width){
    obj.top = Math.min(obj.top, obj.canvas.height-obj.getBoundingRect().height+obj.top-obj.getBoundingRect().top);
    obj.left = Math.min(obj.left, obj.canvas.width-obj.getBoundingRect().width+obj.left-obj.getBoundingRect().left);
  }
});

// create a rect object
var deleteIcon = "/static/img/delete_icon.jpeg";

var cloneIcon = "/static/img/duplicate_icon.jpeg";

var deleteImg = document.createElement('img');
deleteImg.src = deleteIcon;

var cloneImg = document.createElement('img');
cloneImg.src = cloneIcon;

fabric.Object.prototype.transparentCorners = true;
// fabric.Object.prototype.cornerColor = 'black';
// fabric.Object.prototype.cornerStyle = 'circle';

function Add() {
var rect = new fabric.Rect({
  left: 100,
  top: 50,
  fill: 'white',
  width: 150,
  height: 200,
  objectCaching: false,
});

canvas.add(rect);
canvas.setActiveObject(rect);
}

function renderIcon(icon) {
return function renderIcon(ctx, left, top, styleOverride, fabricObject) {
  var size = this.cornerSize;
  ctx.save();
  ctx.translate(left, top);
  ctx.rotate(fabric.util.degreesToRadians(fabricObject.angle));
  ctx.drawImage(icon, -size/2, -size/2, size, size);
  ctx.restore();
}
}

fabric.Object.prototype.controls.deleteControl = new fabric.Control({
x: 0.5,
y: -0.5,
offsetY: -16,
offsetX: 16,
cursorStyle: 'pointer',
mouseUpHandler: deleteObject,
render: renderIcon(deleteImg),
cornerSize: 24
});

fabric.Object.prototype.controls.clone = new fabric.Control({
x: -0.5,
y: -0.5,
offsetY: -16,
offsetX: -16,
cursorStyle: 'pointer',
mouseUpHandler: cloneObject,
render: renderIcon(cloneImg),
cornerSize: 24
});

Add();

function deleteObject(_, target) {
    var canvas = target.canvas;
        canvas.remove(target);
    canvas.requestRenderAll();
}

function cloneObject(_, target) {
var canvas = target.canvas;
target.clone(function(cloned) {
  cloned.left += 10;
  cloned.top += 10;
  canvas.add(cloned);
  canvas.setActiveObject(cloned);
  canvas.bringToFront(cloned)
});
}

function getSpaces(){
    var spaces = [];
    canvas.forEachObject(function(obj){
    var prop = {
        left : obj.left,
        top : obj.top,
        width : obj.width,
        height : obj.height
    };
    spaces.push(prop);
    });
    console.log("Spaces: ", spaces)

    var controlPoint = new fabric.Rect({
        left: 100,
        top: 50,
        fill: 'blue',
        width: 75,
        height: 75,
        objectCaching: false,
        stroke: 'white',
        strokeWidth: 4,
        hasRotatingPoint: false,
        lockRotation: true,
        cornerColor: 'white',
        cornerStyle: 'circle'
      });

      console.log("adding controlPoint")
      canvas.add(controlPoint)
      canvas.setActiveObject(controlPoint);
      
}