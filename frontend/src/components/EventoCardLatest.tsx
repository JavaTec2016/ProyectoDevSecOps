import React from 'react'

export type EventoCardInfo = {
    nombre:string;
    tipo:string;
    fecha_inicio:string;
    fecha_fin:string;
    descripcion:string;
}
export type EventoCardLatestAttribs = {
    info:EventoCardInfo;
    style:React.CSSProperties;
    imgPath:string;
    imgAlt:string;
    onclick?:()=>any;
}
function EventoCardLatest({info, style, imgPath, imgAlt, onclick}:EventoCardLatestAttribs) {
  return (
    <div className='card' style={style} onClick={onclick}>
            <img src={imgPath} className='card-img-top' alt={imgAlt} />
            <div className="badges pb-3">
                <span className="badge text-bg-info">{info.tipo}</span>
            </div>
            <div className="card-body  d-flex flex-column">
                <h5 className="card-text">{info.nombre}</h5>
                <h6 className="card-subtitle text-muted mb-2">{info.fecha_inicio} - {info.fecha_fin}</h6>
                <p className="card-text">
                    {info.descripcion.length > 100 ? (info.descripcion.substring(0,100)+'...') : info.descripcion}
                </p>
            </div>
        </div>
  )
}

export default EventoCardLatest