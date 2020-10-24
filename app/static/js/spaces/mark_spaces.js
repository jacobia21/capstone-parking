/**********************************************
 * Initial Variable Setup
 ***********************************************/
var canvas = (this.__canvas = new fabric.Canvas("c"));
var spaceCount = 0;

var setZonesIcon = "/static/img/set_zones_icon.svg";
var setZonesImg = document.createElement("img");
setZonesImg.src = setZonesIcon;

var plusMinusIcon = "/static/img/plus_minus.svg";
var plusMinusImg = document.createElement("img");
plusMinusImg.src = plusMinusIcon;


var cameraInfo = null;
var canvasImageData = null;
var spacesToRemove = [];

function getCameraInfo(info) {
    cameraInfo = info['cameraInfo'];
    canvasImageData = info['canvasImage']
    if ("spaces" in info) {
        spaces = info["spaces"]
        spaces.forEach((space) => {
            var parkingSpace = new fabric.ParkingSpace({
                width: space.width,
                height: space.height,
                left: space.left,
                top: space.top,
                id: space.id,
                zoneId: space.zoneId,
                fill: "white",
            });
            canvas.add(parkingSpace);
        })
        spaceCount = spaces.length;
        controlPoint = new fabric.ControlPoint({
            width: 75,
            height: 75,
            left: info['controlPoint'].left,
            top: info['controlPoint'].top,
            fill: "lightblue",
        });

        canvas.add(controlPoint)
    }

    return info;
}

function canvasCreation() {

    fabric.Image.fromURL("data:image/jpg;base64," + canvasImageData, function (img) {
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
}

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
    if (spaceCount < 10) {
        var parkingSpace = new fabric.ParkingSpace({
            width: 100,
            height: 150,
            left: 100,
            top: 100,
            fill: "white",
        });
        canvas.add(parkingSpace);
        canvas.setActiveObject(parkingSpace);

        spaceCount += 1;
    } else {
        $("#maxZonesModal").modal("show");
    }
    console.log(spaceCount)

};

/**********************************************
 * Set Zones Handler
 ***********************************************/
const setZonesHandler = (_, object) => {
    var zones = document.getElementsByName("zone");
    console.log(object.zoneId)
    for (var zone of zones) {
        if (object.zoneId === parseInt(zone.value)) {
            console.log(true)
            zone.checked = true;
        } else {
            zone.checked = false;
        }
    }
    $("#setZonesModal").modal("show");
};


/**********************************************
 * Plus Minus Handler
 ***********************************************/
const plusMinusHandler = (_, target) => {
    console.log(target)
    var canvas = target.canvas;
    $("#plusMinusModal").modal("show");
    canvas.requestRenderAll();
};


/**********************************************
 * Set Zones
 ***********************************************/
const setZones = () => {
    let activeObject = canvas.getActiveObject();

    var zones = document.getElementsByName("zone");
    for (var zone of zones) {
        if (zone.checked) {
            activeObject.zoneId = `${zone.value}`
            activeObject.fill = "white"
            canvas.renderAll()
            break
        }
    }
    $("#setZonesModal").modal("hide");
};

const addOrRemoveSpace = () => {
    let selectedValue;
    document.getElementsByName('action').forEach((action) => {
        if (action.checked) {
            selectedValue = action.value
        }
    })
    object = canvas.getActiveObject()
    if (selectedValue === "remove") {
        spaceCount -= 1;
        spacesToRemove.push(object.id)
        canvas.remove(object)
    } else {
        if (spaceCount < 10) {
            object.clone(function (cloned) {
                cloned.left += 10;
                cloned.top += 10;
                cloned.id = 0
                spaceCount = spaceCount + 1;
                canvas.add(cloned);
                canvas.setActiveObject(cloned);
                canvas.bringToFront(cloned);
            });
        } else {
            $("#maxZonesModal").modal("show")
        }
    }
    $("#plusMinusModal").modal("hide");
    console.log(spaceCount)
}
/**********************************************
 * Save Spaces
 ***********************************************/
const saveSpaces = () => {
    parkingSpaces = canvas.getObjects("ParkingSpace");
    allZonesSet = true;


    if (parkingSpaces.length < 1) {
        $("#unsetZonesText")[0].innerText = "No spaces have been added";
        $("#unsetZonesModal").modal("show");
    } else {
        parkingSpaces.forEach((space) => {
            if (space.zoneId === "") {
                allZonesSet = false;

                space.fill = "yellow"
            }
        });

        if (!allZonesSet) {
            $("#unsetZonesText")[0].innerText =
                "You must associate each space with a parking zone. Spaces without a zone are marked in yellow."
            $("#unsetZonesModal").modal("show");
        } else {
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
        canvas.renderAll()
    }
};

/**********************************************
 * ParkingSpace Object Creation
 * ********************************************/
fabric.ParkingSpace = fabric.util.createClass(fabric.Rect, {
    type: "ParkingSpace",
    objectCaching: false,

    initialize: function (options) {
        options || (options = {});
        this.callSuper("initialize", options);
        this.set("id", options.id || 0);
        this.set("zoneId", options.zoneId || "");
        this.set("height", options.height || 150)
        this.set("width", options.width || 100)
    },

    toObject: function () {
        return fabric.util.object.extend(this.callSuper("toObject"), {
            id: this.get("id"),
            zoneId: this.get("zoneId"),
        });
    },

    _render: function (ctx) {
        this.callSuper("_render", ctx);
    },
});

fabric.ParkingSpace.fromObject = function (object, callback) {
    return fabric.Object._fromObject("ParkingSpace", object, callback);
};


fabric.ParkingSpace.prototype.controls.setZones = new fabric.Control({
    x: -0.5,
    y: -0.5,
    offsetX: 15,
    offsetY: 45,
    cursorStyle: "pointer",
    mouseUpHandler: setZonesHandler,
    render: renderIcon(setZonesImg),
    cornerSize: 24,
});


fabric.ParkingSpace.prototype.controls.plusMinus = new fabric.Control({
    x: -0.5,
    y: -0.5,
    offsetX: 15,
    offsetY: 15,
    cursorStyle: "pointer",
    mouseUpHandler: plusMinusHandler,
    render: renderIcon(plusMinusImg),
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
    console.log(data)

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

function updateSpaces(){
    parkingSpaces = canvas.getObjects("ParkingSpace");
    allZonesSet = true;


    if (parkingSpaces.length < 1) {
        $("#unsetZonesText")[0].innerText = "No spaces have been added";
        $("#unsetZonesModal").modal("show");
    } else {
        parkingSpaces.forEach((space) => {
            if (space.zoneId === "") {
                allZonesSet = false;

                space.fill = "yellow"
                canvas.renderAll()
            }
        });

        if (!allZonesSet) {
            $("#unsetZonesText")[0].innerText =
                "You must associate each space with a parking zone. Spaces without a zone are marked in yellow."
            $("#unsetZonesModal").modal("show");
        } else {
            canvasObjects = JSON.stringify(canvas);
            camera = JSON.stringify(cameraInfo);
            data = {camera: camera, canvas: canvasObjects, spacesToRemove:spacesToRemove};

            $.ajax({
                url: "/admin/spaces/update",
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
    }
}