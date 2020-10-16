/**********************************************
 * Initial Variable Setup
 ***********************************************/
var canvas = (this.__canvas = new fabric.Canvas("c"));
var spaceCount = 0;

var setZonesIcon = "/static/img/set_zones_icon.jpg";
var setZonesImg = document.createElement("img");
setZonesImg.src = setZonesIcon;

var deleteIcon = "/static/img/delete_icon.png";
var deleteImg = document.createElement("img");
deleteImg.src = deleteIcon;

var cloneIcon = "/static/img/duplicate_icon.png";
var cloneImg = document.createElement("img");
cloneImg.src = cloneIcon;

var cameraInfo = null;

function getCameraInfo(info) {
    cameraInfo = info;
    return info;
}

fabric.Image.fromURL("/static/img/lot_map.png", function (img) {
    canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas), {
        scaleX: canvas.width / img.width,
        scaleY: canvas.height / img.height,
    });
});

canvas.on("object:moving", function (e) {
    var obj = e.target;
    // if object is too big ignore
    if (
        obj.currentHeight > obj.canvas.height ||
        obj.currentWidth > obj.canvas.width
    ) {
        return;
    }
    obj.setCoords();
    // top-left  corner
    if (obj.getBoundingRect().top < 0 || obj.getBoundingRect().left < 0) {
        obj.top = Math.max(obj.top, obj.top - obj.getBoundingRect().top);
        obj.left = Math.max(obj.left, obj.left - obj.getBoundingRect().left);
    }
    // bot-right corner
    if (
        obj.getBoundingRect().top + obj.getBoundingRect().height >
        obj.canvas.height ||
        obj.getBoundingRect().left + obj.getBoundingRect().width > obj.canvas.width
    ) {
        obj.top = Math.min(
            obj.top,
            obj.canvas.height -
            obj.getBoundingRect().height +
            obj.top -
            obj.getBoundingRect().top
        );
        obj.left = Math.min(
            obj.left,
            obj.canvas.width -
            obj.getBoundingRect().width +
            obj.left -
            obj.getBoundingRect().left
        );
    }
});

/**********************************************
 * Render Icon
 ***********************************************/
const renderIcon = (icon) => {
    return function renderIcon(ctx, left, top, fabricObject) {
        var size = this.cornerSize;
        ctx.save();
        ctx.translate(left, top);
        ctx.rotate(fabric.util.degreesToRadians(fabricObject.angle));
        ctx.drawImage(icon, -size / 2, -size / 2, size, size);
        ctx.restore();
    };
};

/**********************************************
 * Add Space
 ***********************************************/
const addSpace = () => {
    var parkingSpace = new fabric.ParkingSpace({
        width: 100,
        height: 150,
        left: 100,
        top: 100,
        id: spaceCount + 1,
        fill: "white",
    });
    canvas.add(parkingSpace);
    canvas.setActiveObject(parkingSpace);
    spaceCount += 1;
};

/**********************************************
 * Set Zones Handler
 ***********************************************/
const setZonesHandler = (_, object) => {
    var zones = document.getElementsByName("zone");
    for (var zone of zones) {
        if (object.zones.includes(zone.value)) {
            zone.checked = true;
        } else {
            zone.checked = false;
        }
    }
    $("#setZonesModal").modal("show");
};

/**********************************************
 * Delete Space Handler
 ***********************************************/
const deleteSpaceHandler = (_, target) => {
    var canvas = target.canvas;
    canvas.remove(target);
    canvas.requestRenderAll();
};

/**********************************************
 * Clone Space Handler
 ***********************************************/
const cloneSpaceHandler = (_, target) => {
    var canvas = target.canvas;
    // FIXME the cloned object does not currently take the fill color of its original
    target.clone(function (cloned) {
        cloned.left += 10;
        cloned.top += 10;
        cloned.id = spaceCount + 1;
        spaceCount = spaceCount + 1;
        cloned.zones = [];
        canvas.add(cloned);
        canvas.setActiveObject(cloned);
        canvas.bringToFront(cloned);
    });
};

/**********************************************
 * Set Zones
 ***********************************************/
const setZones = () => {
    let activeObject = canvas.getActiveObject();

    var zonesToSet = [];
    var zones = document.getElementsByName("zone");
    for (var zone of zones) {
        if (zone.checked) {
            zonesToSet.push(zone.value);
        }
    }
    activeObject.zones = zonesToSet;
    $("#setZonesModal").modal("hide");
};

/**********************************************
 * Save Spaces
 ***********************************************/
const saveSpaces = () => {
    parkingSpaces = canvas.getObjects("ParkingSpace");
    allZonesSet = true;
    unsetSpaces = [];

    if (parkingSpaces.length < 1) {
        $("#unsetZonesText")[0].innerText = "No spaces have been added";
        $("#unsetZonesModal").modal("show");
    } else {
        parkingSpaces.forEach((space) => {
            if (space.zones.length < 1) {
                allZonesSet = false;
                unsetSpaces.push(space.id);
            }
        });

        if (!allZonesSet) {
            $("#unsetZonesText")[0].innerText =
                "Must add at least one zone to the following space(s): \n" +
                unsetSpaces.toString();
            $("#unsetZonesModal").modal("show");
        } else {
            /* TODO: this is where setting control point should be initiated */

            canvas.getObjects("ParkingSpace").forEach((object) => {
                object.selectable = false;
            });

            controlPoint = new fabric.ControlPoint({
                width: 75,
                height: 75,
                left: 100,
                top: 100,
                fill: "lightblue",
            });
            canvas.add(controlPoint);
            canvas.setActiveObject(controlPoint);
            $(".mark-spaces").addClass("d-none");
            $(".mark-control-point").removeClass("d-none");
        }
    }
};

/**********************************************
 *
 * ParkingSpace Object Creation
 *
 ***********************************************/
fabric.ParkingSpace = fabric.util.createClass(fabric.Rect, {
    type: "ParkingSpace",
    objectCaching: false,

    initialize: function (options) {
        options || (options = {});
        this.callSuper("initialize", options);
        this.set("id", options.id || 0);
        this.set("zones", options.zones || []);
        this.set("height", options.height || 150)
        this.set("width", options.width || 100)
    },

    toObject: function () {
        return fabric.util.object.extend(this.callSuper("toObject"), {
            id: this.get("id"),
            zones: this.get("zones"),
        });
    },

    _render: function (ctx) {
        this.callSuper("_render", ctx);

        ctx.font = "20px Helvetica";
        ctx.fillStyle = "#333";
        ctx.fillText(this.id, this.width / 2 - 20, -this.height / 2 + 20);
    },
});

fabric.ParkingSpace.fromObject = function (object, callback) {
    return fabric.Object._fromObject("ParkingSpace", object, callback);
};

fabric.ParkingSpace.prototype.controls.setZones = new fabric.Control({
    x: -0.5,
    y: -0.5,
    offsetX: 15,
    offsetY: 65,
    cursorStyle: "pointer",
    mouseUpHandler: setZonesHandler,
    render: renderIcon(setZonesImg),
    cornerSize: 24,
});
fabric.ParkingSpace.prototype.controls.deleteControl = new fabric.Control({
    x: -0.5,
    y: -0.5,
    offsetY: 40,
    offsetX: 15,
    cursorStyle: "pointer",
    mouseUpHandler: deleteSpaceHandler,
    render: renderIcon(deleteImg),
    cornerSize: 24,
});

fabric.ParkingSpace.prototype.controls.clone = new fabric.Control({
    x: -0.5,
    y: -0.5,
    offsetY: 15,
    offsetX: 15,
    cursorStyle: "pointer",
    mouseUpHandler: cloneSpaceHandler,
    render: renderIcon(cloneImg),
    cornerSize: 24,
});

/**********************************************
 *
 * Control Point Object Creation
 *
 ***********************************************/
fabric.ControlPoint = fabric.util.createClass(fabric.Rect, {
    type: "ControlPoint",
    objectCaching: false,
    label: "CP",
    hasControls: false,
    hasBorders: false,

    initialize: function (options) {
        options || (options = {});
        this.callSuper("initialize", options);
    },

    toObject: function () {
        return fabric.util.object.extend(this.callSuper("toObject"), {
            label: this.get("label"),
        });
    },

    _render: function (ctx) {
        this.callSuper("_render", ctx);

        ctx.font = "15px Helvetica";
        ctx.fillStyle = "#333";
        ctx.fillText(this.label, -this.width / 2 + 10, -this.height / 2 + 20);
    },
});

fabric.ControlPoint.fromObject = function (object, callback) {
    return fabric.Object._fromObject("ControlPoint", object, callback);
};

function saveAll() {
    canvasObjects = JSON.stringify(canvas);
    camera = JSON.stringify(cameraInfo);
    data = {camera: camera, canvas: canvasObjects};

    $.ajax({
        url: "/admin/spaces/add",
        type: "post",
        data: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
        dataType: "json",
        success: function (data) {
            console.log(data["result"]);
            location.href = "/admin/cameras";
        },
    });
}



let information;
function getInfo(info) {
    information = info
    console.log(information)

    spaces = information["spaces"]
    for (space in spaces){
        var parkingSpace = new fabric.ParkingSpace({
            width: spaces[space].width,
            height: spaces[space].height,
            left: spaces[space].left,
            top: spaces[space].top,
            id: spaces[space].id,
            fill: "white",
        });
        canvas.add(parkingSpace);
    spaceCount = spaces.length;
    }
}
