Schema: flask_capstone
======================


admin_group
-----------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - name
     - name
     - VARCHAR(255)
     - False
     - False
     - None
     - 
   * - description
     - description
     - VARCHAR(255)
     - False
     - False
     - None
     - 

alembic_version
---------------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - version_num
     - version_num
     - VARCHAR(32)
     - True
     - True
     - None
     - 

camera
------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - location
     - location
     - INTEGER
     - False
     - False
     - None
     - 
   * - status
     - status
     - ENUM('ON','OFF')
     - False
     - False
     - None
     - 
   * - lot_id
     - lot_id
     - INTEGER
     - True
     - False
     - None
     - 

Keys
^^^^

* KEY: lot_id (lot_id)

control_points
--------------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - start_x
     - start_x
     - INTEGER
     - False
     - False
     - None
     - 
   * - start_y
     - start_y
     - INTEGER
     - False
     - False
     - None
     - 
   * - end_x
     - end_x
     - INTEGER
     - False
     - False
     - None
     - 
   * - end_y
     - end_y
     - INTEGER
     - False
     - False
     - None
     - 
   * - camera_id
     - camera_id
     - INTEGER
     - True
     - False
     - None
     - 

Keys
^^^^

* KEY: camera_id (camera_id)

logs
----

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - message
     - message
     - VARCHAR(255)
     - False
     - False
     - None
     - 
   * - status
     - status
     - ENUM('OPEN','RESOLVED')
     - False
     - False
     - None
     - 
   * - type
     - type
     - ENUM('WEBSITE','DATBASE','HARDWARE')
     - False
     - False
     - None
     - 
   * - created_at
     - created_at
     - DATETIME
     - True
     - False
     - None
     - 
   * - updated_at
     - updated_at
     - DATETIME
     - False
     - False
     - None
     - 

lot
---

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - name
     - name
     - VARCHAR(100)
     - False
     - False
     - None
     - 

Keys
^^^^

* UNIQUE KEY: ix_lot_name (name)

lotzone
-------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - lot_id
     - lot_id
     - INTEGER
     - True
     - True
     - None
     - 
   * - zone_id
     - zone_id
     - INTEGER
     - True
     - True
     - None
     - 

Keys
^^^^

* KEY: zone_id (zone_id)

space
-----

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - lot_id
     - lot_id
     - INTEGER
     - True
     - False
     - None
     - 
   * - zone_id
     - zone_id
     - INTEGER
     - True
     - False
     - None
     - 
   * - camera_id
     - camera_id
     - INTEGER
     - True
     - False
     - None
     - 
   * - availability
     - availability
     - ENUM('AVAILABLE','NOT_AVAILABLE','RESERVED')
     - False
     - False
     - None
     - 

Keys
^^^^

* KEY: camera_id (camera_id)
* KEY: lot_id (lot_id)
* KEY: zone_id (zone_id)

space_dimensions
----------------

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - start_x
     - start_x
     - INTEGER
     - False
     - False
     - None
     - 
   * - start_y
     - start_y
     - INTEGER
     - False
     - False
     - None
     - 
   * - end_x
     - end_x
     - INTEGER
     - False
     - False
     - None
     - 
   * - end_y
     - end_y
     - INTEGER
     - False
     - False
     - None
     - 
   * - space_id
     - space_id
     - INTEGER
     - True
     - False
     - None
     - 

Keys
^^^^

* KEY: space_id (space_id)

user
----

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - email
     - email
     - VARCHAR(120)
     - False
     - False
     - None
     - 
   * - first_name
     - first_name
     - VARCHAR(255)
     - False
     - False
     - None
     - 
   * - last_name
     - last_name
     - VARCHAR(255)
     - False
     - False
     - None
     - 
   * - middle_initial
     - middle_initial
     - VARCHAR(1)
     - False
     - False
     - None
     - 
   * - password_hash
     - password_hash
     - VARCHAR(128)
     - False
     - False
     - None
     - 
   * - group_id
     - group_id
     - INTEGER
     - False
     - False
     - None
     - 

Keys
^^^^

* UNIQUE KEY: first_name (first_name, last_name, middle_initial)
* KEY: group_id (group_id)
* UNIQUE KEY: ix_user_email (email)
* KEY: ix_user_first_name (first_name)
* KEY: ix_user_last_name (last_name)
* KEY: ix_user_middle_initial (middle_initial)

zone
----

.. list-table::
   :header-rows: 1

   * - Fullname
     - Name
     - Type
     - NOT NULL
     - PKey
     - Default
     - Comment
   * - id
     - id
     - INTEGER
     - True
     - True
     - None
     - 
   * - name
     - name
     - VARCHAR(100)
     - False
     - False
     - None
     - 
   * - color
     - color
     - VARCHAR(100)
     - False
     - False
     - None
     - 

Keys
^^^^

* UNIQUE KEY: ix_zone_color (color)
* UNIQUE KEY: ix_zone_name (name)
