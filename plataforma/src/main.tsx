import { createRoot } from 'react-dom/client'
import { HashRouter } from 'react-router'
import '@fontsource/source-sans-3/400.css'
import '@fontsource/source-sans-3/600.css'
import '@fontsource/source-sans-3/700.css'
import '@fontsource/source-serif-4/600.css'
import '@fontsource/source-serif-4/700.css'
import './index.css'
import './portal.css'
import './tema-c.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(<HashRouter><App /></HashRouter>)
