import {  useEffect, useState, type FC } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { CardHeader, CardText, Button, Form, Alert, Spinner } from "react-bootstrap";
import { LineChart } from "../../components/LineChart";
import { PieChart } from "../../components/PieChart";
import style from "./DashboardPage.module.css";
import API_BASE from "../../config";

interface ISentimentStatusState {
  year: number;
  month: string;
  monthNumber: number;
  negative: number;
  neutral: number;
  positive: number;
}

interface ISentimentTotal {
  negative: number;
  neutral: number;
  positive: number;
}

export const DashboardPage: FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const topic = location.state?.topic || "Тема не выбрана";

  // === Состояния ===
  const [sentimentStatusState, setSentimentStatusState] = useState<ISentimentStatusState[]>([]);
  const [sentimentTotalState, setSentimentTotalState] = useState<ISentimentTotal>({
    negative: 1310,
    neutral: 42,
    positive: 88,
  });
  const [filteredData, setFilteredData] = useState<ISentimentStatusState[]>([]);
  const [filter, setFilter] = useState({ from: "", to: "" });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // === Загрузка данных при монтировании ===
  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const [statsRes, totalRes] = await Promise.all([
          fetch(`${API_BASE}/sentiment-stats?theme=${encodeURIComponent(topic)}`),
          fetch(`${API_BASE}/sentiment-total?theme=${encodeURIComponent(topic)}`),
        ]);

        if (!statsRes.ok || !totalRes.ok) {
          throw new Error("Ошибка при загрузке данных");
        }

        const statsData = await statsRes.json();
        const totalData = await totalRes.json();

        setSentimentStatusState(statsData);
        setFilteredData(statsData); // по умолчанию показываем все данные
        setSentimentTotalState(totalData);
        setError(null);
      } catch (err) {
        console.error("Ошибка API:", err);
        setError("Не удалось загрузить данные. Попробуйте позже.");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [topic]);

  // === Фильтрация данных ===
  function handleFilter(e: React.FormEvent) {
    e.preventDefault();

    if (!filter.from || !filter.to) {
      setError("Пожалуйста, выберите обе даты.");
      return;
    }

    const fromDate = new Date(filter.from);
    const toDate = new Date(filter.to);

    if (fromDate > toDate) {
      setError("Дата начала не может быть позже даты окончания.");
      return;
    }

    const newData = sentimentStatusState.filter((item) => {
      const itemDate = new Date(item.year, item.monthNumber - 1);
      return itemDate >= fromDate && itemDate <= toDate;
    });

    if (newData.length === 0) {
      setError("Данные за выбранный период не найдены.");
      setFilteredData([]);
    } else {
      setError(null);
      setFilteredData(newData);
    }
  }

  // === JSX ===
  return (
    <div className={style.container}>
      <CardHeader as="h2" className={style.title}>
        {topic}
      </CardHeader>

      {/* ===== Секция с LineChart и фильтром ===== */}
      <section className={style.section}>
        <div className={style.chartBox}>
          {loading ? (
            <Spinner animation="border" />
          ) : error && filteredData.length === 0 ? (
            <Alert variant="danger" className={style.alert}>
              {error}
            </Alert>
          ) : (
            <LineChart sentimentStatus={filteredData} />
          )}
        </div>

        <div className={style.infoBox}>
          <Form className={style.filterForm} onSubmit={handleFilter}>
            <Form.Group className={style.filterGroup}>
              <Form.Label>С:</Form.Label>
              <Form.Control
                type="month"
                value={filter.from}
                onChange={(e) => setFilter({ ...filter, from: e.target.value })}
              />
            </Form.Group>

            <Form.Group className={style.filterGroup}>
              <Form.Label>По:</Form.Label>
              <Form.Control
                type="month"
                value={filter.to}
                onChange={(e) => setFilter({ ...filter, to: e.target.value })}
              />
            </Form.Group>

            <Button type="submit" variant="outline-primary" className={style.filterButton}>
              Применить
            </Button>
          </Form>

          {error && filteredData.length > 0 ? (
            <Alert variant="warning">{error}</Alert>
          ) : (
            <CardText>
              Этот график показывает зависимость тональностей отзывов от времени за выбранный период.
            </CardText>
          )}
        </div>
      </section>

      {/* ===== Секция с PieChart ===== */}
      <section className={style.section}>
        <div className={`${style.chartBox} ${style.chartBox__pieChart}`}>
          {loading ? (
            <Spinner animation="border" />
          ) : (
            <PieChart sentimentTotal={sentimentTotalState} />
          )}
        </div>

        <div className={style.infoBox}>
          <CardText>
            Эта круговая диаграмма показывает соотношение тональностей по теме за всё время.
          </CardText>
        </div>
      </section>

      {/* ===== Кнопка возврата ===== */}
      <Button className={style.backButton} onClick={() => navigate("/topics")}>
        Вернуться назад
      </Button>
    </div>
  );
};
