import { useState } from 'react'
import { BarChart3, BookOpen, ExternalLink, Home, Menu, Search, UsersRound, X } from 'lucide-react'
import { NavLink, Outlet, Link, useLocation } from 'react-router'
import CoronelTexture from './CoronelTexture'
import escudoCoronel from '../assets/escudo-coronel-marca.png'

const personalNav = [
  { to: '/personal', label: 'Inicio', icon: Home, tone: 'tone-home' },
  { to: '/panel', label: 'Panel general', icon: BarChart3, tone: 'tone-panel' },
  { to: '/explorador', label: 'Explorador del personal', icon: Search, tone: 'tone-explorer' },
  { to: '/estamento/Planta', label: 'Vistas estamentales', icon: UsersRound, tone: 'tone-estamental' },
  { to: '/metodologia', label: 'Metodología y fuentes', icon: BookOpen, tone: 'tone-method' },
]
const personalPrefixes = ['/personal', '/panel', '/explorador', '/estamento/', '/ficha/', '/metodologia']

export default function Layout() {
  const [open, setOpen] = useState(false)
  const location = useLocation()
  const isPersonal = personalPrefixes.some(prefix => location.pathname.startsWith(prefix))
  const nav = isPersonal ? personalNav : [{ to: '/personal', label: 'Personal y Remuneraciones', icon: UsersRound, tone: 'tone-panel' }]

  return <div className="site-shell">
    <a className="skip-link" href="#contenido">Saltar al contenido</a>
    <div className="institution-bar"><div className="container institution-inner"><span>Municipalidad de Coronel</span><span>Fuente: transparencia activa · MU068 · Ley 20.285 e IGTA</span></div></div>
    <header className="main-header">
      <CoronelTexture variant="mar" />
      <div className="container header-inner">
        <Link to="/" className="brand" aria-label="Portal de Transparencia Trazable, portada" onClick={() => setOpen(false)}>
          <span className="brand-mark"><img src={escudoCoronel} alt="" width={22} height={30} decoding="async" /></span>
          <span><strong>Portal de Transparencia Trazable</strong><small>Municipalidad de Coronel</small></span>
        </Link>
        <button className="menu-button" aria-label={open ? 'Cerrar navegación' : 'Abrir navegación'} aria-expanded={open} onClick={() => setOpen(!open)}>{open ? <X /> : <Menu />}</button>
        <nav className={open ? 'main-nav open' : 'main-nav'} aria-label={isPersonal ? 'Navegación del módulo Personal y Remuneraciones' : 'Navegación principal'}>
          {nav.map(({ to, label, icon: Icon, tone }) => <NavLink key={to} to={to} onClick={() => setOpen(false)} className={({ isActive }) => `nav-link ${tone}${isActive ? ' active' : ''}`}><Icon size={16} />{label}</NavLink>)}
        </nav>
      </div>
    </header>
    <main id="contenido"><Outlet /></main>
    <footer className="site-footer">
      <CoronelTexture variant="industria" />
      <div className="container footer-mainline">
        <strong>Portal de Transparencia Trazable</strong>
        <span className="footer-compass">Toda cifra perseguible hasta su fuente · Toda ausencia declarada.</span>
        <nav className="footer-links" aria-label="Origen y método">
          <a href="https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=MU068" target="_blank" rel="noreferrer">Portal municipal MU068 <ExternalLink size={13} aria-hidden="true" /></a>
          <Link to="/actualizaciones">Actualizaciones</Link>
          <Link to="/metodologia">Metodología y ausencias de Personal</Link>
        </nav>
      </div>
      <div className="container footer-license">
        <p>Código: <a href="https://opensource.org/license/mit" target="_blank" rel="noreferrer">MIT</a> · Datos agregados y artefactos derivados: <a href="https://creativecommons.org/licenses/by/4.0/deed.es" target="_blank" rel="noreferrer">CC-BY 4.0</a> · Atribución: Portal de Transparencia Trazable — Municipalidad de Coronel.</p>
        {isPersonal && <p className="glossary-global-note"><span aria-hidden="true">¡</span> El símbolo ¡ abre una tarjeta con la definición del término y su fuente normativa.</p>}
      </div>
    </footer>
  </div>
}
