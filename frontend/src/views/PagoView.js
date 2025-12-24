const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const data = {
      empleado_id: selectedEmpleadoId,
      monto_base: parseFloat(formData.monto_base),
      extras: parseFloat(formData.extras)
    };
    await pagosAPI.create(data);
    alert("Pago registrado con éxito");
  } catch (err) {
    setError(err.response?.data?.error || "Error al procesar pago");
  }
};