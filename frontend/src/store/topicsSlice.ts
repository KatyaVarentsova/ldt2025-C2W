import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"
import API_BASE from "../config"

export interface ITopic {
    idCategory: number,
    themeCategory: string
}

interface ITopicsState {
    topics: ITopic[]
}

const topicsState : ITopicsState = {
    topics: [
        {
            idCategory: 1,
            themeCategory: "Банкоматы",
        }, 
        {
            idCategory: 2,
            themeCategory: "Дебетовые карты",
        },
        {
            idCategory: 3,
            themeCategory: "Кешбэк и бонусы",
        },
        {
            idCategory: 4,
            themeCategory: "Комиссии и тарифы",
        },
        {
            idCategory: 5,
            themeCategory: "Кредитные карты",
        },
        {
            idCategory: 6,
            themeCategory: "Кредиты и займы",
        },
        {
            idCategory: 7,
            themeCategory: "Мобильное приложение",
        },
        {
            idCategory: 8,
            themeCategory: "Обслуживание в офисах",
        },
        {
            idCategory: 9,
            themeCategory: "Переводы и платежи",
        },
        {
            idCategory: 10,
            themeCategory: "Техподдержка",
        },
    ]
}

export const fetchTopics = createAsyncThunk('topicsSlice/fetchTopics', (_, thunkObject) => {
    fetch(`${API_BASE}/themes`)
        .then((result) => {
            return result.json()
        })
        .then((result) => {
            const dispatch = thunkObject.dispatch;
            dispatch(saveTopics(result))
        })
})

const topicsSlice = createSlice({
    name: 'topicsSlice',
    initialState: topicsState,
    reducers: {
        saveTopics: (state, action) => {
            state.topics = [...action.payload]
        }
    },
    selectors: {
        topicsSelector: (state) => state.topics
    }
})

export default topicsSlice.reducer
export const {saveTopics} = topicsSlice.actions
export const {topicsSelector} = topicsSlice.selectors