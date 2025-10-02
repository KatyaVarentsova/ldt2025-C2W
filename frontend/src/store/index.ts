import { configureStore } from "@reduxjs/toolkit";
import { useDispatch, useSelector, type TypedUseSelectorHook } from "react-redux";
import topicsSlice from "./topicsSlice"
import commonsStartsSlice from "./commonStartsSlice"

const store = configureStore({
    reducer: {
       topicsSlice: topicsSlice,
       commonsStartsSlice: commonsStartsSlice,
    }
})

export default store
//RootState - это тип переменной store
export type RootState = ReturnType<typeof store.getState>;
//Функция для изменения состояния
export const useAppDispatch: () => typeof store.dispatch = useDispatch
//Функция для чтения состояния
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector