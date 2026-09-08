import React, { useEffect, useState } from 'react'
import { Navigation } from '../components/Navigation'
import { Nav } from 'react-bootstrap'
import Breadcrumb from '../components/Breadcrumb'
import API from '../api/api'
import EventoCardLatest, { type EventoCardInfo } from '../components/EventoCardLatest'

function ColectasPage() {
    const [eventos, setEventos] = useState<{ [x: string]: any }[]>([]);
    const [loading, setLoading] = useState(true);
    //=========EVENTAR
    function getEventos() {
        const eventus: { [x: string]: any }[] = [];
        API.get(API.EVENTOS + API.LATEST_END, null).then(res => {
            res.data.forEach((row:{[x:string]:any}) => {
                const ev = {
                    nombre: row.nombre,
                    tipo: row.tipo,
                    fecha_inicio: row.fecha_inicio,
                    fecha_fin: row.fecha_fin,
                    descripcion: row.descripcion,
                }
                eventus.push(ev);
            })

        }).then(() => {
            setEventos(eventus);
            setLoading(false);
        })
    }
    useEffect(()=>getEventos(), []);
    useEffect(()=>{
        console.log(eventos);
    }, [eventos])
    return (
        <div className='app-shell'>
            <Navigation includeSidebar={true}>
                <Nav>
                    <Nav.Link href="#top">Inicio</Nav.Link>
                </Nav>
            </Navigation>
            <Breadcrumb path="colectas" />

            <main className="page-content">
                <section className="mb-4">
                    <h2 className="fw-bold mb-1">Eventos recientes</h2>
                    <p className="text-muted mb-3">
                        Descubre los últimos eventos disponibles. Explora fechas, tipos y detalles de cada actividad.
                    </p>
                    <hr />
                </section>

                {loading ? (
                    <div className="d-flex justify-content-center py-5">
                        <div className="spinner-border text-primary" role="status">
                            <span className="visually-hidden">Cargando eventos...</span>
                        </div>
                    </div>
                ) : eventos.length === 0 ? (
                    <p className="text-center text-muted py-5">No hay eventos disponibles.</p>
                ) : (
                    <div className="row row-cols-1 row-cols-md-2 row-cols-xl-3 g-4">
                        {eventos.map((evento, index) => (
                            <div className="col" key={index}>
                                <EventoCardLatest
                                    info={evento as EventoCardInfo}
                                    style={{ height: '100%' }}
                                    imgPath={'../assets/img/c carros 8k.png'}
                                    imgAlt={`Imagen de ${evento.nombre}`}
                                />
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    )
}

export default ColectasPage