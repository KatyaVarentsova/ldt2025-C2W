import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import type { FC } from 'react';
import { Pie } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

interface ISentimentTotal {
  negative: number,
  neutral: number,
  positive: number
}

interface IPieChartProps {
  sentimentTotal: ISentimentTotal
}

export const PieChart: FC<IPieChartProps> = ({sentimentTotal}) => {
  const data = {
    labels: ['Положительные', 'Нейтральные', 'Отрицательные'],
    datasets: [
      {
        label: 'Кол-во комментариев',
        data: [sentimentTotal.positive, sentimentTotal.neutral, sentimentTotal.negative],
        backgroundColor: [
          '#8DAAFF',
          '#FFDC89',
          '#FF8C8C',
        ],
        borderColor: [
          '#365FDB',
          '#D9AF4E',
          '#A63C3C',
        ],
        borderWidth: 1,
      },
    ],
  };
  return <Pie data={data} width={400} height={300} />;
}
