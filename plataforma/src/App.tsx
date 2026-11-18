import { useEffect, useState } from 'react'
import { Route, Routes, useLocation } from 'react-router'
import type { CommonData } from './types'
import { loadCommonData } from './lib/data'
import { SourceProvider } from './components/Source'
import { ErrorState, Loading } from './components/Common'
import Layout from './components/Layout'
import Home from './pages/Home'
import Panel from './pages/Panel'
import Explorador from './pages/Explorador'
import Estamental from './pages/Estamental'
import Ficha from './pages/Ficha'
import Metodologia from './pages/Metodologia'
import PortalHome from './pages/PortalHome'
import Actualizaciones from './pages/Actualizaciones'

export default function App() {
  const [data, setData] = useState<CommonData | null>(null)
  const [error, setError] = useState('')
  const [attempt, setAttempt] = useState(0)
  const location = useLocation()
  useEffect(() => { window.scrollTo({ top: 0, behavior: 'instant' }) }, [location.pathname])
  useEffect(() => {
    let active = true
    loadCommonData().then(result => { if (active) setData(result) }).catch(reason => { if (active) setError(reason.message) })
    return () => { active = false }
  }, [attempt])
  const retry = () => { setError(''); setData(null); setAttempt(value => value + 1) }
  return <SourceProvider>
    {error ? <ErrorState message={error} retry={retry} /> : !data ? <Loading /> : <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<PortalHome />} />
        <Route path="/personal" element={<Home data={data} />} />
        <Route path="/panel" element={<Panel data={data} />} />
        <Route path="/explorador" element={<Explorador data={data} />} />
        <Route path="/estamento/:categoria" element={<Estamental data={data} />} />
        <Route path="/ficha/:id" element={<Ficha data={data} />} />
        <Route path="/metodologia" element={<Metodologia data={data} />} />
        <Route path="/actualizaciones" element={<Actualizaciones />} />
        <Route path="*" element={<PortalHome />} />
      </Route>
    </Routes>}
  </SourceProvider>
}
