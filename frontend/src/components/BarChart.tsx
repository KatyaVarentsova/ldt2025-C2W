import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { useAppSelector } from '../store';
import { commonsStartsSelector } from '../store/commonStartsSlice';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export function BarChart() {
  const commonsStarts = useAppSelector(commonsStartsSelector);

  const labels = commonsStarts.map((item) => item.month + ' ' + item.year);

  const data = {
    labels,
    datasets: [
      {
        label: '1 звезда',
        data: commonsStarts.map((item) => item.star1),
        backgroundColor: '#EE5555',
      },
      {
        label: '2 звезды',
        data: commonsStarts.map((item) => item.star2),
        backgroundColor: '#EB8E4B',
      },
      {
        label: '3 звезды',
        data: commonsStarts.map((item) => item.star3),
        backgroundColor: '#EEC159',
      },
      {
        label: '4 звезды',
        data: commonsStarts.map((item) => item.star4),
        backgroundColor: '#4FBFEF',
      },
      {
        label: '5 звёзд',
        data: commonsStarts.map((item) => item.star5),
        backgroundColor: '#4068E4',
      },
    ],
  };

  const options = {
    plugins: {
      title: {
        display: true,
        text: 'Динамика оценок по месяцам',
        font: {
          size: 18,
        },
      },
      legend: {
        position: 'bottom' as const,
      },
    },
    responsive: true,
    scales: {
      x: {
        stacked: true,
        title: {
          display: true,
          text: 'Месяцы',
        },
      },
      y: {
        stacked: true,
        title: {
          display: true,
          text: 'Количество отзывов',
        },
      },
    },
  };

  return (
    <div style={{ width: '100%', maxWidth: '900px', margin: '0 auto' }}>
      <Bar options={options} data={data} />
    </div>
  );
}
