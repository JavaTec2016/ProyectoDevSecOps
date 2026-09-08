import React from 'react'
import type { FormRows } from '../components/forms/FormComponent'
import type { CrudComponentAttributes } from '../components/CrudComponent'
import API from '../api/api'
import { Nav } from 'react-bootstrap'
import { Navigation } from '../components/Navigation'
import Breadcrumb from '../components/Breadcrumb'
import CrudComponent from '../components/CrudComponent'

const labels = {
    anio_graduacion:'Año de graduación'
}
const formConfig:FormRows = [
    [
        {
            field:'anio_graduacion',
            config:{
                name:'input',
                type:'number',
                label: labels['anio_graduacion']
            }
        }
    ]
]
const crudAttributes: CrudComponentAttributes = {
    formRows:formConfig,
    createFormPresentation: {
        title: 'Nueva Clase',
        subtitle: 'Ingrese la informacion'
    },
    updateFormPresentation: {
        title: 'Actualizar Clase',
        subtitle: 'Ingrese la informacion'
    },
    validators: {
        anio_graduacion: {
            required: "Campo requerido",
            maxLength: { value: 5, message: "No puede superar 5 dígitos" },
            minLength: { value: 4, message: "Debe ser menor a 4 dígitos" },
            pattern: {
                value: /^[0-9]+$/,
                message: "Sólo se permiten números",
            },
        },
    },
    labelSchema: labels,
    detailLayout: [['anio_graduacion']],
    detailPresentation: {
        title: 'Detalles de la Clase',
        subtitle: 'Informacion'
    },
    tableColumns: ['anio_graduacion'],
    primaryKey: 'anio_graduacion',
    tablePresentation: {
        title: 'Clases',
        subtitle: 'Listado',
    },
    endpoint: API.CLASES,
    createMessages: {
        success: 'Clase creada'
    },
    updateMessages: {
        success: 'Clase actualizada'
    },
    deleteMessages: {
        confirmation: 'Desea eliminar la Clase? cualquier registro asociado sera eliminado',
        success: 'Clase eliminado'
    },
    serverErrorMessage: 'Error del servidor, intentelo mas tarde'
}
function ClasesPage() {
  return (
    <div className="app-shell">
            <Navigation includeSidebar={true}>
                <Nav>
                    <Nav.Link href="#top">Inicio</Nav.Link>
                    <Nav.Link href="/colectas">Colectas</Nav.Link>
                </Nav>
            </Navigation>
            <Breadcrumb path="colectas/clases" />

            <main className="page-content">
                <CrudComponent
                    attributes={crudAttributes}
                />
            </main>
        </div>
  )
}

export default ClasesPage