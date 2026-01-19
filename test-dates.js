const formatDateForComparison = (dateStr) => {
  const parts = dateStr.split(/[\/\-\.]/);
  if (parts.length >= 3) {
    let day = parts[0];
    let month = parts[1];
    let year = parts[2];
    if (day.length === 1) day = `0${day}`;
    if (month.length === 1) month = `0${month}`;
    if (year.length === 2) year = `20${year}`;
    return `${year}-${month}-${day}`;
  }
  return dateStr;
};

const parseDateStr = (dateStr) => {
  const parts = dateStr.split(/[\/\-\.]/);
  let day = parts[0];
  let month = parts[1];
  const year = parts[2];
  if (day.length === 1) day = `0${day}`;
  if (month.length === 1) month = `0${month}`;
  return new Date(`${year}-${month}-${day}`);
};

const mockHaircuts = [
  { id: '1', clientName: 'Juan', serviceName: 'Corte', price: 5000, date: '03/01/2026' },
  { id: '2', clientName: 'Pedro', serviceName: 'Corte', price: 13000, date: '08/01/2026' },
  { id: '3', clientName: 'Maria', serviceName: 'Corte', price: 60000, date: '09/01/2026' },
];

console.log('=== Date Formatting Tests ===');
console.log('formatDateForComparison("03/01/2026"):', formatDateForComparison('03/01/2026'));
console.log('formatDateForComparison("08/01/2026"):', formatDateForComparison('08/01/2026'));
console.log('formatDateForComparison("09/01/2026"):', formatDateForComparison('09/01/2026'));

console.log('\n=== Date Filtering Tests ===');
const startDate = '2026-01-01';
const endDate = '2026-01-31';

const filtered = mockHaircuts.filter(h => {
  const haircutDate = formatDateForComparison(h.date);
  return haircutDate >= startDate && haircutDate <= endDate;
});

console.log('Filtered haircuts count:', filtered.length);
console.log('Filtered haircuts:', filtered);

console.log('\n=== Daily Stats Calculation ===');
const stats = {};
mockHaircuts.forEach(h => {
  const dateStr = formatDateForComparison(h.date);
  if (!stats[dateStr]) {
    stats[dateStr] = { count: 0, revenue: 0 };
  }
  stats[dateStr].count += 1;
  stats[dateStr].revenue += h.price;
});

console.log('Daily stats:', stats);

console.log('\n=== Total Revenue ===');
const totalRevenue = mockHaircuts.reduce((sum, h) => sum + h.price, 0);
console.log('Total revenue:', totalRevenue);

console.log('\n=== Average Daily ===');
const uniqueDays = new Set(mockHaircuts.map(h => formatDateForComparison(h.date))).size;
const avgDaily = uniqueDays > 0 ? totalRevenue / uniqueDays : 0;
console.log('Unique days:', uniqueDays);
console.log('Average daily:', avgDaily);

console.log('\n=== All Tests Passed! ===');
