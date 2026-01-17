import { useCallback, useState } from 'react';
import * as XLSX from 'xlsx';
import { HaircutCreate } from '../types';
import { haircutService } from '../services/haircutService';

interface ExcelRow {
  FECHA: string;
  CORTE: string | number;
}

interface ExcelImporterProps {
  onImportComplete: () => void;
}

export function ExcelImporter({ onImportComplete }: ExcelImporterProps) {
  const [preview, setPreview] = useState<HaircutCreate[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [importing, setImporting] = useState(false);
  const [success, setSuccess] = useState(false);

  const parsePrice = (priceStr: string | number): number => {
    if (typeof priceStr === 'number') return priceStr;
    const cleaned = priceStr.replace(/[$.\s]/g, '').replace(/,/g, '.');
    return parseFloat(cleaned) || 0;
  };

  const parseDate = (dateStr: string): string => {
    const currentYear = new Date().getFullYear();
    const parts = dateStr.split('/');
    if (parts.length === 2) {
      return `${parts[0].padStart(2, '0')}/${parts[1].padStart(2, '0')}/${currentYear}`;
    }
    return dateStr;
  };

  const handleFileUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setError(null);
    setSuccess(false);

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = e.target?.result;
        const workbook = XLSX.read(data, { type: 'binary' });
        const sheetName = workbook.SheetNames[0];
        const worksheet = workbook.Sheets[sheetName];
        const rows: any[][] = XLSX.utils.sheet_to_json(worksheet, { header: 1 }) as any[][];

        const parsedData: HaircutCreate[] = rows
          .slice(1)
          .filter((row: any) => row[0] && row[1])
          .map((row: any) => ({
            name: 'Corte',
            price: parsePrice(row[1]),
            date: parseDate(row[0].toString()),
          }));

        if (parsedData.length === 0) {
          setError('No se encontraron datos válidos en el archivo');
          setPreview([]);
        } else {
          setPreview(parsedData);
        }
      } catch (err) {
        setError('Error al leer el archivo. Asegúrate de que sea un archivo Excel válido.');
        setPreview([]);
      }
    };
    reader.readAsBinaryString(file);
  }, []);

  const handleImport = async () => {
    if (preview.length === 0) return;

    setImporting(true);
    setError(null);

    try {
      for (const item of preview) {
        await haircutService.create(item);
      }
      setSuccess(true);
      setPreview([]);
      onImportComplete();
    } catch (err) {
      setError('Error al importar los datos. Por favor intenta nuevamente.');
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="excel-importer">
      <div className="importer-header">
        <h3>Importar desde Excel</h3>
        <p>Formato esperado: columna FECHA y columna CORTE (monto)</p>
      </div>

      <div className="file-input-container">
        <input
          type="file"
          accept=".xlsx,.xls,.csv"
          onChange={handleFileUpload}
          className="file-input"
          id="excel-file"
        />
        <label htmlFor="excel-file" className="file-label">
          📁 Seleccionar archivo
        </label>
      </div>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">¡Datos importados exitosamente!</div>}

      {preview.length > 0 && (
        <div className="preview-container">
          <h4>Vista previa ({preview.length} registros)</h4>
          <div className="preview-table-wrapper">
            <table className="preview-table">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Monto</th>
                </tr>
              </thead>
              <tbody>
                {preview.slice(0, 10).map((item, index) => (
                  <tr key={index}>
                    <td>{item.date}</td>
                    <td>${item.price.toLocaleString('es-AR')}</td>
                  </tr>
                ))}
                {preview.length > 10 && (
                  <tr>
                    <td colSpan={2}>... y {preview.length - 10} más</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          <button
            onClick={handleImport}
            disabled={importing}
            className="import-btn"
          >
            {importing ? 'Importando...' : `Importar ${preview.length} registros`}
          </button>
        </div>
      )}
    </div>
  );
}
