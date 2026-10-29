from django.urls import path
from .views import *

urlpatterns = [

    # --------------------------- Usuario --------------------------
    path('usuarios/', UsuarioListCreateView.as_view(), name='usuario-list-create'),
    path('usuarios/<str:usuario_id>/',
         UsuarioDetailView.as_view(), name='usuario-detail'),

    # ---------------------- Empresa ------------------
    path('empresas/', EmpresaListCreateView.as_view(), name='empresa-list-create'),
    path('empresas/<str:empresa_id>/',
         EmpresaDetailView.as_view(), name='empresa-detail'),

    # ---------------------- Vinculación ------------------
    path('vinculaciones/', VinculacionListCreateView.as_view(),
         name='vinculacion-list-create'),
    path('vinculaciones/<str:vinculacion_id>/',
         VinculacionDetailView.as_view(), name='vinculacion-detail'),

    # ---------------------- Producto ------------------
    path('productos/', ProductoListCreateView.as_view(), name='producto-list-create'),
    path('productos/<str:producto_id>/',
         ProductoDetailView.as_view(), name='producto-detail'),

    # ---------------------- Pedido ------------------
    path('pedidos/', PedidoListCreateView.as_view(), name='pedido-list-create'),
    path('pedidos/<str:pedido_id>/', PedidoDetailView.as_view(), name='pedido-detail'),

    # ---------------------- Conductor ------------------
    path('conductores/', ConductorListCreateView.as_view(), name='conductor-list-create'),
    path('conductores/<str:conductor_id>/',
         ConductorDetailView.as_view(), name='conductor-detail'),

    # ---------------------- Recepción ------------------
    path('recepciones/', RecepcionListCreateView.as_view(), name='recepcion-list-create'),
    path('recepciones/<str:recepcion_id>/',
         RecepcionDetailView.as_view(), name='recepcion-detail'),

    # ---------------------- Inventario ------------------
    path('inventarios/', InventarioListCreateView.as_view(),
         name='inventario-list-create'),
    path('inventarios/<str:inventario_id>/',
         InventarioDetailView.as_view(), name='inventario-detail'),

    # ---------------------- Docking ------------------
    path('dockings/', DockingListCreateView.as_view(), name='docking-list-create'),
    path('dockings/<str:docking_id>/',
         DockingDetailView.as_view(), name='docking-detail'),

    # ---------------------- Alistamiento ------------------
    path('alistamientos/', AlistamientoListCreateView.as_view(),
         name='alistamiento-list-create'),
    path('alistamientos/<str:alistamiento_id>/',
         AlistamientoDetailView.as_view(), name='alistamiento-detail'),

    # ---------------------- Despacho ------------------
    path('despachos/', DespachoListCreateView.as_view(), name='despacho-list-create'),
    path('despachos/<str:despacho_id>/',
         DespachoDetailView.as_view(), name='despacho-detail')

]
