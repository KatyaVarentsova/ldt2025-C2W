import { type FC } from "react";
import { Button, CardText } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import style from "./HomePage.module.css"


export const HomePage: FC = () => {
    const navigate = useNavigate();

    const handleClick = () => {
        navigate("/common")
    }

    return (
        <>
            <CardText>Все комментарии для анализа взяты с <a href="https://www.sravni.ru/bank/gazprombank/otzyvy/" target="_blank">sravni.ru</a> и <a href="https://www.banki.ru/services/responses/bank/gazprombank/?is_countable=on" target="_blank">banki.ru</a>.</CardText>
            <Button onClick={handleClick} className={style.backButton}>Провести анализ комментариев</Button>
        </>

    )
}