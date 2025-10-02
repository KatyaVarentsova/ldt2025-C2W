import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"
import API_BASE from "../config"

export interface ICommonStars {
    year: number,
    month: string,
    monthNumber: number,
    star1: number,
    star2: number,
    star3: number,
    star4: number,
    star5: number,
}

interface ICommonsStarsState {
    commonsStarts: ICommonStars[]
}

const commonsStartsState : ICommonsStarsState = {
    commonsStarts: [
    {
        year: 2024,
        month: "Январь",
        monthNumber: 1,
        star1: 547,
        star2: 81,
        star3: 29,
        star4: 26,
        star5: 227
    },
    {
        year: 2024,
        month: "Февраль",
        monthNumber: 2,
        star1: 592,
        star2: 115,
        star3: 39,
        star4: 5,
        star5: 207
    },
    {
        year: 2024,
        month: "Март",
        monthNumber: 3,
        star1: 792,
        star2: 133,
        star3: 55,
        star4: 33,
        star5: 156
    },
    {
        year: 2024,
        month: "Апрель",
        monthNumber: 4,
        star1: 1008,
        star2: 130,
        star3: 77,
        star4: 43,
        star5: 176
    },
    {
        year: 2024,
        month: "Май",
        monthNumber: 5,
        star1: 1070,
        star2: 182,
        star3: 60,
        star4: 49,
        star5: 195
    },
    {
        year: 2024,
        month: "Июнь",
        monthNumber: 6,
        star1: 1107,
        star2: 216,
        star3: 59,
        star4: 36,
        star5: 144
    },
    {
        year: 2024,
        month: "Июль",
        monthNumber: 7,
        star1: 1377,
        star2: 206,
        star3: 79,
        star4: 43,
        star5: 150
    },
    {
        year: 2024,
        month: "Август",
        monthNumber: 8,
        star1: 1747,
        star2: 262,
        star3: 80,
        star4: 37,
        star5: 99
    },
    {
        year: 2024,
        month: "Сентябрь",
        monthNumber: 9,
        star1: 2041,
        star2: 240,
        star3: 73,
        star4: 29,
        star5: 119
    },
    {
        year: 2024,
        month: "Октябрь",
        monthNumber: 10,
        star1: 3077,
        star2: 346,
        star3: 103,
        star4: 22,
        star5: 97
    },
    {
        year: 2024,
        month: "Ноябрь",
        monthNumber: 11,
        star1: 2408,
        star2: 381,
        star3: 104,
        star4: 43,
        star5: 121
    },
    {
        year: 2024,
        month: "Декабрь",
        monthNumber: 12,
        star1: 1724,
        star2: 294,
        star3: 76,
        star4: 34,
        star5: 127
    },
    {
        year: 2025,
        month: "Январь",
        monthNumber: 1,
        star1: 1126,
        star2: 210,
        star3: 35,
        star4: 31,
        star5: 98
    },
    {
        year: 2025,
        month: "Февраль",
        monthNumber: 2,
        star1: 1196,
        star2: 144,
        star3: 26,
        star4: 34,
        star5: 101
    },
    {
        year: 2025,
        month: "Март",
        monthNumber: 3,
        star1: 926,
        star2: 102,
        star3: 45,
        star4: 21,
        star5: 83
    },
    {
        year: 2025,
        month: "Апрель",
        monthNumber: 4,
        star1: 693,
        star2: 115,
        star3: 35,
        star4: 12,
        star5: 121
    },
    {
        year: 2025,
        month: "Май",
        monthNumber: 5,
        star1: 567,
        star2: 57,
        star3: 12,
        star4: 22,
        star5: 126
    }
]

}

export const fetchCommonsStarts = createAsyncThunk('commonsStartsSlice/fetchCommonsStarts', (_, thunkObject) => {
    fetch(`${API_BASE}/rating-stats`)
        .then((result) => {
            return result.json()
        })
        .then((result) => {
            const dispatch = thunkObject.dispatch;
            dispatch(saveCommonsStarts(result))
        })
})

const commonsStartsSlice = createSlice({
    name: 'commonsStartsSlice',
    initialState: commonsStartsState,
    reducers: {
        saveCommonsStarts: (state, action) => {
            state.commonsStarts = [...action.payload]
        }
    },
    selectors: {
        commonsStartsSelector: (state) => state.commonsStarts 
    }
})

export default commonsStartsSlice.reducer
export const {saveCommonsStarts} = commonsStartsSlice.actions
export const {commonsStartsSelector} = commonsStartsSlice.selectors

