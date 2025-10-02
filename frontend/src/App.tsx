import { Route, Routes } from 'react-router-dom'
import './App.css'
import { DashboardPage } from './pages/DashboardPage/DashboardPage'
import { HomePage } from './pages/HomePage/HomePage'
import { CommonPage } from './pages/CommonPage/CommonPage'
import { TopicsPage } from './pages/TopicsPage/TopicsPage'
import { useEffect } from 'react'
import { useAppDispatch } from './store'
import { fetchTopics } from './store/topicsSlice'
import { fetchCommonsStarts } from './store/commonStartsSlice'

function App() {

  const dispatch = useAppDispatch()

    useEffect(() => {
        dispatch(fetchTopics())
        dispatch(fetchCommonsStarts())
    }, [])


  return (
    <>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/common" element={<CommonPage/>} />
        <Route path="/topics" element={<TopicsPage/>} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>

    </>
  )
}

export default App
