import type { FC } from "react";
import { BarChart } from "../../components/BarChart";
import { useNavigate } from "react-router-dom";
import { Button, CardHeader, CardText } from "react-bootstrap";
import style from "./CommonPage.module.css";

export const CommonPage: FC = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/topics");
  };

  return (
    <div className={style.commonPage}>
      <CardHeader as="h2" className={style.commonPage__title}>
        Общий анализ
      </CardHeader>

      <div className={style.commonPage__content}>
        <div className={style.commonPage__chart}>
          <BarChart />
        </div>
        <div className={style.commonPage__description}>
          <CardText>
            Этот график демонстрирует изменение уровня лояльности клиентов по месяцам, что позволяет оценить динамику их приверженности к вашему продукту или услуге.
          </CardText>
        </div>
      </div>

      <Button className={style.commonPage__button} onClick={handleClick}>
        Перейти к выбору темы
      </Button>
    </div>
  );
};