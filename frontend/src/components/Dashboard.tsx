import React, { useState } from 'react';
import { Haircut, HaircutCreate } from '../types';
import { HaircutForm } from './HaircutForm';
import { HaircutList } from './HaircutList';
import { DailyHistoryList } from './DailyHistoryList';
import { PriceEditor } from './PriceEditor';
import { useHaircuts, useDailySummary } from '../hooks/useHaircuts';

export function Dashboard() {
  const { haircuts, loading, error, addHaircut, updateHaircut, updatePrice, deleteHaircut } =
    useHaircuts();
  const { summary, history, refetch: refetchSummary } = useDailySummary();
  const [editingHaircut, setEditingHaircut] = useState<Haircut | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingPrice, setEditingPrice] = useState<string | null>(null);
  const [newPrice, setNewPrice] = useState<string>('');
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleCreate = () => {
    setEditingHaircut(null);
    setShowForm(true);
  };

  const handleEdit = (haircut: Haircut) => {
    setEditingHaircut(haircut);
    setShowForm(true);
  };

  const handleSubmit = async (haircutData: HaircutCreate) => {
    try {
      if (editingHaircut) {
        await updateHaircut({ ...haircutData, id: editingHaircut.id });
      } else {
        await addHaircut(haircutData);
      }
      setShowForm(false);
      setEditingHaircut(null);
      refetchSummary();
    } catch (err) {
      console.error('Error saving haircut:', err);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteHaircut(id);
      refetchSummary();
    } catch (err) {
      console.error('Error deleting haircut:', err);
    }
  };

  const handlePriceEdit = (id: string, currentPrice: number) => {
    setEditingPrice(id);
    setNewPrice(currentPrice.toString());
  };

  const handlePriceSave = async (id: string) => {
    const price = parseFloat(newPrice);
    if (isNaN(price) || price < 0) {
      alert('Por favor ingresa un precio válido');
      return;
    }
    try {
      await updatePrice(id, price);
      setEditingPrice(null);
      setNewPrice('');
      refetchSummary();
    } catch (err) {
      console.error('Error updating price:', err);
    }
  };

  const handleCancelPriceEdit = () => {
    setEditingPrice(null);
    setNewPrice('');
  };

  const handleDeleteToday = async () => {
    if (!summary) return;
    if (!confirm(`¿Estás seguro de eliminar todos los ${summary.count} cortes de hoy?`)) {
      return;
    }
    try {
      await haircutService.deleteByDate(summary.date);
      refetchSummary();
      await useHaircuts().refetch();
    } catch (err) {
      console.error('Error deleting today\'s haircuts:', err);
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingHaircut(null);
  };

  const formatCurrency = (amount: number) => {
    if (isNaN(amount) || amount === null || amount === undefined) {
      return '$0,00';
    }
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
    }).format(amount);
  };

  return (
    <div className="dashboard">
      <h1>Barbershop Management</h1>

      {error && <div className="error-message">{error}</div>}

      <div className="summary-cards">
        <div className="summary-card today">
          <h3>Hoy</h3>
          {loading ? (
            <p>Cargando...</p>
          ) : (
            <>
              <p className="count">{summary?.count || 0} cortes</p>
              <p className="total">{formatCurrency(summary?.total || 0)}</p>
            </>
          )}
        </div>
        <div className="summary-card currency">
          <h3>Moneda</h3>
          <p>Pesos Argentinos (ARS)</p>
        </div>
        <div className="summary-card actions-card">
          <h3>Acciones Rápidas</h3>
          <button onClick={handleCreate} className="action-btn create">
            + Nuevo Corte
          </button>
          {summary && summary.count > 0 && (
            <button onClick={handleDeleteToday} className="action-btn delete-all">
              Eliminar Hoy
            </button>
          )}
        </div>
      </div>

      {showForm && (
        <div className="form-container">
          <h2>{editingHaircut ? 'Editar Corte' : 'Nuevo Corte'}</h2>
          <HaircutForm
            onSubmit={handleSubmit}
            initialData={editingHaircut || undefined}
            onCancel={handleCancel}
          />
        </div>
      )}

      <div className="main-content">
        <div className="haircuts-section">
          <h2>Cortes del Día</h2>
          {loading ? (
            <p>Cargando...</p>
          ) : haircuts.length === 0 ? (
            <div className="empty-state">
              <p>No hay cortes registrados.</p>
              <button onClick={handleCreate} className="create-btn">
                Agregar Primer Corte
              </button>
            </div>
          ) : (
            <HaircutList
              haircuts={haircuts}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onEditPrice={handlePriceEdit}
            />
          )}
          {editingPrice && (
            <PriceEditor
              currentPrice={parseFloat(newPrice)}
              newPrice={newPrice}
              onNewPriceChange={setNewPrice}
              onSave={() => handlePriceSave(editingPrice)}
              onCancel={handleCancelPriceEdit}
            />
          )}
        </div>

        <div className="history-section">
          <DailyHistoryList history={history} />
        </div>
      </div>
    </div>
  );
}
