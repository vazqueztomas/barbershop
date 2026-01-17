import { useMemo } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts';
import { Haircut } from '../types';

interface StatisticsProps {
  haircuts: Haircut[];
}

interface DailyStats {
  date: string;
  dayName: string;
  revenue: number;
  count: number;
  avgPrice: number;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

const getDayName = (dateStr: string): string => {
  const date = new Date(dateStr);
  const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
  return days[date.getDay()];
};

const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export function Statistics({ haircuts }: StatisticsProps) {
  const dailyStats: DailyStats[] = useMemo(() => {
    const last7Days: DailyStats[] = [];
    const today = new Date();

    for (let i = 6; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      const dateStr = date.toISOString().split('T')[0];
      const dayName = getDayName(dateStr);

      const dayHaircuts = haircuts.filter((h) => h.date === dateStr);
      const revenue = dayHaircuts.reduce((sum, h) => sum + h.price, 0);
      const count = dayHaircuts.length;
      const avgPrice = count > 0 ? revenue / count : 0;

      last7Days.push({
        date: dateStr,
        dayName,
        revenue,
        count,
        avgPrice,
      });
    }

    return last7Days;
  }, [haircuts]);

  const serviceStats = useMemo(() => {
    const serviceMap = new Map<string, { count: number; revenue: number }>();

    haircuts.forEach((haircut) => {
      const service = haircut.name;
      const existing = serviceMap.get(service) || { count: 0, revenue: 0 };
      serviceMap.set(service, {
        count: existing.count + 1,
        revenue: existing.revenue + haircut.price,
      });
    });

    const totalCount = haircuts.length;
    const stats = Array.from(serviceMap.entries()).map(([name, data]) => ({
      name,
      count: data.count,
      revenue: data.revenue,
      percentage: totalCount > 0 ? (data.count / totalCount) * 100 : 0,
    }));

    return stats.sort((a: { count: number }, b: { count: number }) => b.count - a.count);
  }, [haircuts]);

  const totalRevenue = useMemo(
    () => haircuts.reduce((sum, h) => sum + h.price, 0),
    [haircuts]
  );

  const avgDaily = useMemo(() => {
    const uniqueDays = new Set(haircuts.map((h) => h.date)).size;
    return uniqueDays > 0 ? totalRevenue / uniqueDays : 0;
  }, [haircuts, totalRevenue]);

  const topService = serviceStats[0];

  return (
    <div className="statistics">
      <div className="stats-summary">
        <div className="summary-stat">
          <span className="label">Total Ingresos</span>
          <span className="value">{formatCurrency(totalRevenue)}</span>
        </div>
        <div className="summary-stat">
          <span className="label">Total Cortes</span>
          <span className="value">{haircuts.length}</span>
        </div>
        <div className="summary-stat">
          <span className="label">Promedio Diario</span>
          <span className="value">{formatCurrency(avgDaily)}</span>
        </div>
        <div className="summary-stat">
          <span className="label">Servicio Popular</span>
          <span className="value">{topService?.name || '-'}</span>
          <span className="sublabel">{topService?.count || 0} cortes</span>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-card">
          <h3>Ingresos Ultimos 7 Dias</h3>
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={dailyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="dayName" />
              <YAxis tickFormatter={(value) => `$${Number(value) / 1000}k`} />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="revenue"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Cantidad de Cortes por Dia</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={dailyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="dayName" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#82ca9d" name="Cortes" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Distribucion por Servicio</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={serviceStats}
                dataKey="count"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
              >
                {serviceStats.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Cortes por Dia</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={dailyStats}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="dayName" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="count"
                stroke="#0088FE"
                name="Cortes"
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="revenue"
                stroke="#00C49F"
                name="Ingresos"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="stats-table-container">
        <h3>Detalle por Servicio</h3>
        <table className="stats-table">
          <thead>
            <tr>
              <th>Servicio</th>
              <th>Cantidad</th>
              <th>Ingresos</th>
              <th>Participacion</th>
            </tr>
          </thead>
          <tbody>
            {serviceStats.map((service) => (
              <tr key={service.name}>
                <td>{service.name}</td>
                <td>{service.count}</td>
                <td>{formatCurrency(service.revenue)}</td>
                <td>
                  <div className="progress-bar">
                    <div
                      className="progress-fill"
                      style={{ width: `${service.percentage}%` }}
                    />
                    <span>{service.percentage.toFixed(1)}%</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
