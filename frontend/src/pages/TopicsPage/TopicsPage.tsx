import type { FC } from "react";
import { Button, CardHeader } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import style from "./TopicsPage.module.css"
import { useAppSelector } from "../../store";
import { topicsSelector } from "../../store/topicsSlice";

export const TopicsPage: FC = () => {
  const topics = useAppSelector(topicsSelector)

  const navigate = useNavigate();

  const handleClick = (topic: string) => {
    console.log("Выбрана тема:", topic);
    navigate("/dashboard", { state: { topic } });
  };

  return (
    <div className={style.topicsPage}>
      <CardHeader as="h2" className={style.topicsPage__title}>
        Выберите тему
      </CardHeader>

      <div className={style.topicsPage__grid}>
        {topics.map((item) => (
          <Button
            key={item.idCategory}
            onClick={() => handleClick(item.themeCategory)}
            variant="outline-primary"
            className={style.topicsPage__button}
          >
            {item.themeCategory}
          </Button>
        ))}
      </div>

      <Button
        className={style.topicsPage__backButton}
        onClick={() => navigate("/common")}
      >
        Вернуться назад
      </Button>
    </div>
  );
};