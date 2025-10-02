import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import type { FC } from "react";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface ISentimentStatus {
  year: number;
  month: string;
  monthNumber: number;
  negative: number;
  neutral: number;
  positive: number;
}

interface ILineChartProps {
  sentimentStatus: ISentimentStatus[];
}

export const LineChart: FC<ILineChartProps> = ({ sentimentStatus }) => {
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
      },
      title: {
        display: true,
        text: "Динамика тональностей по месяцам",
      },
    },
  };

  // Формируем подписи оси X из данных
  const labels = sentimentStatus.map((item) => item.month + ' ' + item.year);

  // Формируем наборы данных для линий
  const data = {
    labels,
    datasets: [
      {
        label: "Положительные",
        data: sentimentStatus.map((item) => item.positive),
        borderColor: "#8DAAFF",
        backgroundColor: "#8DAAFF",
      },
      {
        label: "Нейтральные",
        data: sentimentStatus.map((item) => item.neutral),
        borderColor: "#FFDC89",
        backgroundColor: "#FFDC89",
      },
      {
        label: "Отрицательные",
        data: sentimentStatus.map((item) => item.negative),
        borderColor: "#FF8C8C",
        backgroundColor: "#FF8C8C",
      },
    ],
  };

  return <Line options={options} data={data} />;
};
