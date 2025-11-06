# 🎯 Gestión de Usuarios - Endpoints Centralizados en Admin

## ✅ **MIGRACIÓN COMPLETADA**

Se ha centralizado toda la funcionalidad de usuarios en `admin_routes.py` y se eliminó `usuario_routes.py` según tu solicitud.

## 📋 **ENDPOINTS DISPONIBLES**

### 1. 📊 **Dashboard/Estadísticas**
```
GET /api/admin/stats
Authorization: Bearer {token_admin}
```

### 2. ➕ **Crear Usuario**
```
POST /api/admin/crear-usuarios
Authorization: Bearer {token_admin}
Content-Type: application/json
```

**Body:**
```json
{
  "nombre_completo": "Juan Pérez García",
  "usuario": "juan_rrhh",
  "dni": "12345678",
  "rol": "rrhh"
}
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Usuario creado exitosamente",
  "usuario": {
    "id": 3,
    "nombre_completo": "Juan Pérez García",
    "usuario": "juan_rrhh",
    "dni": "12345678",
    "rol": "rrhh"
  }
}
```

### 3. 📋 **Listar Usuarios**
```
GET /api/admin/usuarios
Authorization: Bearer {token_admin}
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "usuario": "admin",
    "dni": "00000000",
    "rol": "administrador"
  },
  {
    "id": 2,
    "usuario": "juan_rrhh",
    "dni": "12345678",
    "rol": "rrhh"
  }
]
```

### 4. 🔍 **Obtener Usuario por ID**
```
GET /api/admin/usuarios/{usuario_id}
Authorization: Bearer {token_admin}
```

**Respuesta:**
```json
{
  "id": 2,
  "nombre_completo": "Juan Pérez García",
  "usuario": "juan_rrhh",
  "dni": "12345678",
  "rol": "rrhh"
}
```

### 5. ✏️ **Actualizar Usuario**
```
PUT /api/admin/modificar-usuarios/{usuario_id}
Authorization: Bearer {token_admin}
Content-Type: application/json
```

**Body (campos opcionales):**
```json
{
  "nombre_completo": "Juan Carlos Pérez",
  "usuario": "juan_admin",
  "dni": "87654321",
  "rol": "administrador"
}
```

### 6. 🗑️ **Eliminar Usuario**
```
DELETE /api/admin/eliminar-usuarios/{usuario_id}
Authorization: Bearer {token_admin}
```

## 🎯 **FLUJO COMPLETO DE EDICIÓN**

### Para tu React Frontend:

```javascript
// 1. Cargar lista de usuarios
const usuarios = await fetch('/api/admin/usuarios', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// 2. Cuando usuario hace clic en "Editar"
const cargarDatosUsuario = async (usuarioId) => {
  const response = await fetch(`/api/admin/usuarios/${usuarioId}`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const userData = await response.json();
  
  // 3. Pre-llenar formulario
  setFormData({
    nombre_completo: userData.nombre_completo,
    usuario: userData.usuario,
    dni: userData.dni,
    rol: userData.rol
  });
};

// 4. Guardar cambios
const guardarCambios = async (usuarioId, datosModificados) => {
  const response = await fetch(`/api/admin/modificar-usuarios/${usuarioId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(datosModificados)
  });
  
  return response.json();
};
```

## 🛡️ **VALIDACIONES IMPLEMENTADAS**

### Crear Usuario
- ✅ **Usuario único**: No permite duplicar nombres de usuario
- ✅ **DNI único**: No permite duplicar DNIs
- ✅ **Campos obligatorios**: Todos los campos son requeridos

### Actualizar Usuario
- ✅ **Usuario existe**: Verifica que el ID sea válido
- ✅ **Usuario único**: No permite duplicar con otros usuarios
- ✅ **DNI único**: No permite duplicar con otros usuarios
- ✅ **Actualización parcial**: Solo actualiza campos enviados

### Eliminar Usuario
- ✅ **Usuario existe**: Verifica que el ID sea válido
- ✅ **Último admin**: Protege contra eliminar el último administrador
- ✅ **Autorización**: Solo administradores pueden eliminar

## 📁 **ARCHIVOS MODIFICADOS**

### ✅ Eliminados:
- `app/routes/usuario_routes.py` ❌ (eliminado)
- `app/controllers/usuario_controller.py` ❌ (eliminado)

### ✅ Actualizados:
- `app/routes/admin_routes.py` ✅ (centralizado todo)
- `app/controllers/admin_controller.py` ✅ (funciones mejoradas)
- `app/schemas/usuario_schema.py` ✅ (esquemas añadidos)

## 🔗 **ESTRUCTURA FINAL**

```
📁 app/
├── 📁 routes/
│   ├── admin_routes.py      ✅ (CRUD completo usuarios)
│   ├── auth_routes.py       ✅ (login)
│   └── rrhh_routes.py       ✅ (papeletas)
├── 📁 controllers/
│   ├── admin_controller.py  ✅ (lógica usuarios)
│   ├── auth_controller.py   ✅ (autenticación)
│   └── papeleta_controller.py ✅ (papeletas)
└── 📁 schemas/
    ├── usuario_schema.py    ✅ (todos los esquemas)
    └── papeleta_schema.py   ✅ (esquemas papeletas)
```

## 🎉 **LISTO PARA USAR**

Ahora toda la gestión de usuarios está centralizada en `/api/admin/` como solicitaste:

- ✅ **Crear**: `POST /api/admin/crear-usuarios`
- ✅ **Listar**: `GET /api/admin/usuarios`
- ✅ **Obtener**: `GET /api/admin/usuarios/{id}`
- ✅ **Editar**: `PUT /api/admin/modificar-usuarios/{id}`
- ✅ **Eliminar**: `DELETE /api/admin/eliminar-usuarios/{id}`

¡Todo funciona correctamente y está listo para integrar con tu frontend React! 🚀