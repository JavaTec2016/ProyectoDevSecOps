import React from 'react'
import type { FormRows } from '../components/forms/FormComponent'
import type { CrudComponentAttributes } from '../components/CrudComponent'
import API from '../api/api'
import { Navigation } from '../components/Navigation'
import { Nav } from 'react-bootstrap'
import Breadcrumb from '../components/Breadcrumb'
import CrudComponent from '../components/CrudComponent'

const labels = {
    id:"ID",
    username:"Usuario",
    password:"Contraseña",
    rol:"Rol",
    is_active: 'Habilitado'
}
const formConfig: FormRows = [
    [
        {
            field:'username',
            config:{
                name:'input',
                type:'text',
                label:labels['username']
            }
        }
    ],
    [
        {
            field:'password',
            config:{
                name:'input',
                type:'text',
                label:labels['password']
            }
        }
    ],
    [
        {
            field:'rol',
            config:{
                name:'select',
                options:{'':'Seleccionar...', 'admin':'Administrador','usuario':'Usuario'},
                label:labels['rol']
            }
        }
    ]
]
const crudAttributes: CrudComponentAttributes = {
    formRows: formConfig,
    createFormPresentation: {
        title: 'Nuevo Usuario',
        subtitle: 'Ingrese la informacion'
    },
    updateFormPresentation: {
        title: 'Actualizar Usuario',
        subtitle: 'Ingrese la informacion'
    },
    validators: {
        usuername: {
            required: "Campo requerido",
            maxLength: { value: 100, message: "No puede superar 100 caracteres" },
            pattern: {
                value: /^[0-9A-Za-z ]+$/,
                message: "Solo se permiten numeros, espacios y letras",
            }
        },
        password: {
            required: "Campo requerido",
            maxLength: { value: 100, message: "No puede superar 100 caracteres" },
        },
    },
    labelSchema: labels,
    detailLayout: [['id', 'username'], ['rol'], ['is_active']],
    detailPresentation: {
        title: 'Detalles del Usuario',
        subtitle: 'Informacion'
    },
    tableColumns: ['username', 'rol', 'is_active'],
    primaryKey: 'id',
    tablePresentation: {
        title: 'Usuario',
        subtitle: 'Listado',
    },

    endpoint: API.USUARIOS,
    createMessages: {
        success: 'Usuario creado'
    },
    updateMessages: {
        success: 'Usuario actualizado'
    },
    deleteMessages: {
        confirmation: 'Desea eliminar el Usuario? cualquier registro asociado sera eliminado',
        success: 'Usuario eliminado'
    },
    serverErrorMessage: 'Error del servidor, intentelo mas tarde'
}
function UsuariosPage() {
  return (
        <div className="app-shell">
            <Navigation includeSidebar={true}>
                <Nav>
                    <Nav.Link href="#top">Inicio</Nav.Link>
                    <Nav.Link href="/colectas">Colectas</Nav.Link>
                </Nav>
            </Navigation>
            <Breadcrumb path="/eventos" />

            <main className="page-content">
                <CrudComponent
                    attributes={crudAttributes}
                />
            </main>
        </div>
  )
}

export default UsuariosPage