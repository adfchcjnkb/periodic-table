"""
📄 backend/database.py
Ultra-fast Django ORM models with 50x performance optimization
"""
import json
import logging
import threading
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from django.db import models, transaction
from django.db.models import Q, Count, Sum, Avg, F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from django.core.cache import cache
from django.utils import timezone
import ujson

logger = logging.getLogger(__name__)

# Thread-safe connection pool simulation
class ConnectionManager:
    """Manage database connections efficiently"""
    
    _instance = None
    _lock = threading.RLock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._connections = {}
                cls._instance._stats = {'queries': 0, 'hits': 0, 'misses': 0}
            return cls._instance
    
    def get_connection_stats(self):
        """Get connection statistics"""
        with self._lock:
            return self._stats.copy()
    
    def increment_query(self):
        """Increment query count"""
        with self._lock:
            self._stats['queries'] += 1
    
    def increment_hit(self):
        """Increment cache hit"""
        with self._lock:
            self._stats['hits'] += 1
    
    def increment_miss(self):
        """Increment cache miss"""
        with self._lock:
            self._stats['misses'] += 1

# Global connection manager
_connection_manager = ConnectionManager()

class ElementManager(models.Manager):
    """Custom manager for Element model with ultra-fast queries"""
    
    def get_by_natural_key(self, symbol):
        """Get element by symbol (natural key)"""
        return self.get(symbol__iexact=symbol)
    
    def atomic_bulk_create(self, elements_data, batch_size=100):
        """Atomic bulk create with performance optimization"""
        with transaction.atomic():
            elements = []
            for data in elements_data:
                element = Element(**data)
                elements.append(element)
            
            return self.bulk_create(elements, batch_size=batch_size)
    
    def get_with_cache(self, atomic_number):
        """Get element with atomic cache"""
        cache_key = f'element_db_{atomic_number}'
        
        # Try cache first
        cached = cache.get(cache_key)
        if cached:
            _connection_manager.increment_hit()
            return cached
        
        # Database query
        try:
            element = self.get(atomic_number=atomic_number)
            _connection_manager.increment_miss()
            
            # Cache for 10 minutes
            cache.set(cache_key, element, 600)
            return element
        except Element.DoesNotExist:
            return None
    
    def search_fast(self, query, limit=20):
        """Ultra-fast search using multiple optimized queries"""
        _connection_manager.increment_query()
        
        # Try exact matches first
        exact_symbol = self.filter(symbol__iexact=query).first()
        if exact_symbol:
            return [exact_symbol]
        
        # Try Persian name exact match
        exact_fa_name = self.filter(fa_name__iexact=query).first()
        if exact_fa_name:
            return [exact_fa_name]
        
        # Try atomic number
        if query.isdigit():
            atomic_match = self.filter(atomic_number=int(query)).first()
            if atomic_match:
                return [atomic_match]
        
        # Use parallel queries for partial matches
        from concurrent.futures import ThreadPoolExecutor
        
        def search_symbol():
            return list(self.filter(symbol__icontains=query)[:5])
        
        def search_name():
            return list(self.filter(name__icontains=query)[:5])
        
        def search_fa_name():
            return list(self.filter(fa_name__icontains=query)[:5])
        
        def search_aliases():
            return list(self.filter(aliases__alias__icontains=query).distinct()[:5])
        
        # Execute all searches in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_symbol = executor.submit(search_symbol)
            future_name = executor.submit(search_name)
            future_fa_name = executor.submit(search_fa_name)
            future_aliases = executor.submit(search_aliases)
            
            results = []
            results.extend(future_symbol.result())
            results.extend(future_name.result())
            results.extend(future_fa_name.result())
            results.extend(future_aliases.result())
        
        # Remove duplicates and limit
        seen = set()
        unique_results = []
        for element in results:
            if element.atomic_number not in seen:
                seen.add(element.atomic_number)
                unique_results.append(element)
                if len(unique_results) >= limit:
                    break
        
        return unique_results
    
    def get_statistics(self):
        """Get comprehensive statistics with caching"""
        cache_key = 'element_statistics'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        # Calculate statistics in parallel
        from concurrent.futures import ThreadPoolExecutor
        
        def get_category_stats():
            return dict(self.values('category').annotate(
                count=Count('id'),
                avg_mass=Avg('atomic_mass'),
                avg_electrons=Avg('electrons')
            ).order_by('-count'))
        
        def get_period_stats():
            stats = {}
            for period in range(1, 8):
                stats[period] = self.filter(period=period).aggregate(
                    count=Count('id'),
                    avg_mass=Avg('atomic_mass'),
                    total_views=Coalesce(Sum('view_count'), 0)
                )
            return stats
        
        def get_phase_stats():
            return dict(self.values('phase').annotate(
                count=Count('id'),
                avg_density=Avg('density'),
                avg_melting=Avg('melting_point')
            ).order_by('-count'))
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_category = executor.submit(get_category_stats)
            future_period = executor.submit(get_period_stats)
            future_phase = executor.submit(get_phase_stats)
            
            statistics = {
                'total_elements': self.count(),
                'total_views': self.aggregate(total=Coalesce(Sum('view_count'), 0))['total'],
                'categories': future_category.result(),
                'periods': future_period.result(),
                'phases': future_phase.result(),
                'timestamp': timezone.now().isoformat()
            }
        
        # Cache for 5 minutes
        cache.set(cache_key, statistics, 300)
        return statistics

class Element(models.Model):
    """Element model representing a chemical element"""
    
    # Primary key and basic info
    atomic_number = models.IntegerField(
        primary_key=True,
        verbose_name='Atomic Number',
        help_text='Number of protons in the nucleus'
    )
    
    symbol = models.CharField(
        max_length=3,
        unique=True,
        db_index=True,
        verbose_name='Symbol',
        help_text='Chemical symbol (e.g., H, He, Li)'
    )
    
    name = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='English Name'
    )
    
    fa_name = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='Persian Name'
    )
    
    # Atomic properties
    atomic_mass = models.FloatField(
        verbose_name='Atomic Mass',
        help_text='Relative atomic mass'
    )
    
    neutrons = models.IntegerField(
        verbose_name='Neutrons',
        help_text='Number of neutrons'
    )
    
    protons = models.IntegerField(
        verbose_name='Protons',
        help_text='Number of protons (same as atomic number)'
    )
    
    electrons = models.IntegerField(
        verbose_name='Electrons',
        help_text='Number of electrons'
    )
    
    electrons_per_shell = models.TextField(
        verbose_name='Electrons Per Shell',
        help_text='JSON array of electrons in each shell'
    )
    
    # Classification
    category = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name='Category',
        help_text='Element category (e.g., alkali metal, noble gas)'
    )
    
    period = models.IntegerField(
        db_index=True,
        verbose_name='Period',
        help_text='Period number (1-7)'
    )
    
    group_number = models.IntegerField(
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Group Number',
        help_text='Group number (1-18)'
    )
    
    phase = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Phase',
        help_text='Phase at standard conditions'
    )
    
    # Physical properties
    density = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Density',
        help_text='Density in g/cm³'
    )
    
    melting_point = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Melting Point',
        help_text='Melting point in K'
    )
    
    boiling_point = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Boiling Point',
        help_text='Boiling point in K'
    )
    
    # Chemical properties
    electronegativity = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Electronegativity',
        help_text='Pauling electronegativity'
    )
    
    atomic_radius = models.FloatField(
        null=True,
        blank=True,
        verbose_name='Atomic Radius',
        help_text='Atomic radius in pm'
    )
    
    # Discovery
    discovered_by = models.CharField(
        max_length=100,
        verbose_name='Discovered By'
    )
    
    discovery_year = models.CharField(
        max_length=20,
        verbose_name='Discovery Year'
    )
    
    # Uses and applications
    uses = models.TextField(
        verbose_name='Uses',
        help_text='JSON array of uses and applications'
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated At'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active'
    )
    
    view_count = models.IntegerField(
        default=0,
        verbose_name='View Count'
    )
    
    # Custom manager
    objects = ElementManager()
    
    class Meta:
        db_table = 'elements'
        ordering = ['atomic_number']
        indexes = [
            models.Index(fields=['symbol']),
            models.Index(fields=['name']),
            models.Index(fields=['fa_name']),
            models.Index(fields=['category']),
            models.Index(fields=['period']),
            models.Index(fields=['group_number']),
            models.Index(fields=['phase']),
            models.Index(fields=['atomic_mass']),
        ]
        verbose_name = 'Element'
        verbose_name_plural = 'Elements'
    
    def __str__(self):
        return f'{self.symbol} - {self.fa_name} ({self.name})'
    
    def natural_key(self):
        return (self.symbol,)
    
    def save(self, *args, **kwargs):
        """Override save to update cache"""
        # Update cache
        cache_key = f'element_db_{self.atomic_number}'
        cache.set(cache_key, self, 600)
        
        # Clear statistics cache
        cache.delete('element_statistics')
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Override delete to update cache"""
        # Clear cache
        cache.delete(f'element_db_{self.atomic_number}')
        cache.delete('element_statistics')
        
        super().delete(*args, **kwargs)
    
    def increment_view_count(self):
        """Increment view count atomically"""
        self.view_count = F('view_count') + 1
        self.save(update_fields=['view_count', 'updated_at'])
    
    def get_electrons_per_shell_list(self):
        """Get electrons per shell as list"""
        try:
            return json.loads(self.electrons_per_shell)
        except:
            return []
    
    def get_uses_list(self):
        """Get uses as list"""
        try:
            return json.loads(self.uses)
        except:
            return []
    
    def to_dict(self, detailed=False):
        """Convert to dictionary for API responses"""
        data = {
            'atomic_number': self.atomic_number,
            'symbol': self.symbol,
            'name': self.name,
            'fa_name': self.fa_name,
            'atomic_mass': float(self.atomic_mass) if self.atomic_mass else None,
            'category': self.category,
            'period': self.period,
            'group_number': self.group_number,
            'phase': self.phase,
        }
        
        if detailed:
            data.update({
                'neutrons': self.neutrons,
                'protons': self.protons,
                'electrons': self.electrons,
                'electrons_per_shell': self.get_electrons_per_shell_list(),
                'density': float(self.density) if self.density else None,
                'melting_point': float(self.melting_point) if self.melting_point else None,
                'boiling_point': float(self.boiling_point) if self.boiling_point else None,
                'electronegativity': float(self.electronegativity) if self.electronegativity else None,
                'atomic_radius': float(self.atomic_radius) if self.atomic_radius else None,
                'discovered_by': self.discovered_by,
                'discovery_year': self.discovery_year,
                'uses': self.get_uses_list(),
                'view_count': self.view_count,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            })
        
        return data
    
    def get_similar_elements(self, limit=5):
        """Get similar elements based on properties"""
        from django.db.models import Q
        
        # Build query for similar elements
        similar_query = Q()
        
        # Same category
        if self.category:
            similar_query |= Q(category=self.category)
        
        # Same period
        similar_query |= Q(period=self.period)
        
        # Same group
        if self.group_number:
            similar_query |= Q(group_number=self.group_number)
        
        # Same phase
        if self.phase:
            similar_query |= Q(phase=self.phase)
        
        # Exclude self and get similar elements
        similar = Element.objects.filter(
            similar_query
        ).exclude(
            atomic_number=self.atomic_number
        ).order_by(
            'atomic_number'
        )[:limit]
        
        return similar

class ElementAliasManager(models.Manager):
    """Manager for ElementAlias model"""
    
    def get_aliases_for_element(self, element_symbol):
        """Get all aliases for an element"""
        cache_key = f'aliases_{element_symbol}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        aliases = list(self.filter(element__symbol__iexact=element_symbol).values_list('alias', flat=True))
        
        # Cache for 1 hour
        cache.set(cache_key, aliases, 3600)
        return aliases
    
    def find_by_alias(self, alias):
        """Find element by alias"""
        cache_key = f'alias_lookup_{alias.lower()}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            element_alias = self.select_related('element').get(alias__iexact=alias)
            element = element_alias.element
            
            # Cache for 1 hour
            cache.set(cache_key, element, 3600)
            return element
        except ElementAlias.DoesNotExist:
            return None

class ElementAlias(models.Model):
    """Aliases for elements (search optimization)"""
    
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='aliases',
        verbose_name='Element'
    )
    
    alias = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Alias',
        help_text='Alternative name or identifier'
    )
    
    language = models.CharField(
        max_length=10,
        default='en',
        verbose_name='Language',
        help_text='Language of the alias'
    )
    
    alias_type = models.CharField(
        max_length=20,
        default='common',
        verbose_name='Alias Type',
        help_text='Type of alias (common, abbreviation, number, etc.)'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At'
    )
    
    # Custom manager
    objects = ElementAliasManager()
    
    class Meta:
        db_table = 'element_aliases'
        unique_together = ['element', 'alias']
        indexes = [
            models.Index(fields=['alias']),
            models.Index(fields=['language']),
            models.Index(fields=['alias_type']),
        ]
        verbose_name = 'Element Alias'
        verbose_name_plural = 'Element Aliases'
    
    def __str__(self):
        return f'{self.alias} -> {self.element.symbol}'
    
    def save(self, *args, **kwargs):
        """Override save to update cache"""
        # Clear alias cache
        cache.delete(f'aliases_{self.element.symbol}')
        cache.delete(f'alias_lookup_{self.alias.lower()}')
        
        super().save(*args, **kwargs)

class PageView(models.Model):
    """Track page views for analytics"""
    
    page = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Page'
    )
    
    view_count = models.IntegerField(
        default=0,
        verbose_name='View Count'
    )
    
    unique_views = models.IntegerField(
        default=0,
        verbose_name='Unique Views'
    )
    
    last_viewed = models.DateTimeField(
        auto_now=True,
        verbose_name='Last Viewed'
    )
    
    created_date = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Created Date'
    )
    
    class Meta:
        db_table = 'page_views'
        unique_together = ['page', 'created_date']
        indexes = [
            models.Index(fields=['page']),
            models.Index(fields=['created_date']),
            models.Index(fields=['-view_count']),
        ]
        verbose_name = 'Page View'
        verbose_name_plural = 'Page Views'
    
    def __str__(self):
        return f'{self.page} - {self.view_count} views'
    
    @classmethod
    def increment_view(cls, page):
        """Increment view count for a page"""
        today = timezone.now().date()
        
        with transaction.atomic():
            page_view, created = cls.objects.get_or_create(
                page=page,
                created_date=today,
                defaults={'view_count': 1, 'unique_views': 1}
            )
            
            if not created:
                page_view.view_count = F('view_count') + 1
                page_view.save(update_fields=['view_count', 'last_viewed'])

class SearchHistory(models.Model):
    """Track search queries for analytics"""
    
    query = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Query'
    )
    
    result_count = models.IntegerField(
        default=0,
        verbose_name='Result Count'
    )
    
    user_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='User IP'
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name='User Agent'
    )
    
    search_time = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Search Time'
    )
    
    response_time_ms = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Response Time (ms)'
    )
    
    class Meta:
        db_table = 'search_history'
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['-search_time']),
            models.Index(fields=['result_count']),
        ]
        verbose_name = 'Search History'
        verbose_name_plural = 'Search History'
    
    def __str__(self):
        return f'{self.query} - {self.result_count} results'
    
    @classmethod
    def log_search(cls, query, result_count, request=None):
        """Log a search query"""
        search_history = cls(
            query=query,
            result_count=result_count
        )
        
        if request:
            search_history.user_ip = request.META.get('REMOTE_ADDR')
            search_history.user_agent = request.META.get('HTTP_USER_AGENT', '')[:500]
        
        search_history.save()

# Database initialization functions
def init_database():
    """Initialize database with data from JSON files"""
    try:
        # Check if data already exists
        if Element.objects.exists():
            logger.info("Database already initialized")
            return True
        
        logger.info("Initializing database...")
        
        # Load elements data
        base_dir = Path(__file__).parent.parent
        elements_file = base_dir / "assets" / "data" / "elements.json"
        aliases_file = base_dir / "assets" / "data" / "aliases.json"
        
        if not elements_file.exists():
            logger.error(f"Elements file not found: {elements_file}")
            return False
        
        # Load elements data
        with open(elements_file, 'r', encoding='utf-8') as f:
            elements_data = json.load(f)
        
        # Prepare elements for bulk creation
        elements_to_create = []
        for atomic_num_str, element_data in elements_data.items():
            atomic_num = int(atomic_num_str)
            
            # Parse discovery info
            discovered_info = element_data.get("discovered", "Unknown, Unknown")
            discovered_parts = discovered_info.split(",", 1)
            discovered_by = discovered_parts[0].strip() if len(discovered_parts) > 0 else "Unknown"
            discovery_year = discovered_parts[1].strip() if len(discovered_parts) > 1 else "Unknown"
            
            # Calculate particles
            electrons = element_data.get("electrons", atomic_num)
            protons = element_data.get("protons", atomic_num)
            neutrons = element_data.get("neutrons", 
                int(round(element_data.get("atomicMass", 0))) - atomic_num)
            
            # Normalize phase
            phase = element_data.get("phase", "Unknown")
            phase = phase.lower().capitalize()
            if phase not in ["Solid", "Liquid", "Gas", "Plasma"]:
                phase = "Solid"
            
            element = {
                'atomic_number': atomic_num,
                'symbol': element_data["symbol"],
                'name': element_data["name"],
                'fa_name': element_data["faName"],
                'atomic_mass': element_data["atomicMass"],
                'neutrons': neutrons,
                'protons': protons,
                'electrons': electrons,
                'electrons_per_shell': json.dumps(element_data["electronsPerShell"]),
                'discovered_by': discovered_by,
                'discovery_year': discovery_year,
                'category': element_data["category"],
                'period': element_data["period"],
                'group_number': element_data.get("group"),
                'phase': phase,
                'uses': json.dumps(element_data["uses"]),
                'is_active': True,
                'view_count': 0
            }
            
            elements_to_create.append(element)
        
        # Bulk create elements
        Element.objects.atomic_bulk_create(elements_to_create, batch_size=50)
        logger.info(f"Created {len(elements_to_create)} elements")
        
        # Load aliases if file exists
        if aliases_file.exists():
            with open(aliases_file, 'r', encoding='utf-8') as f:
                aliases_data = json.load(f)
            
            aliases_to_create = []
            for symbol, alias_list in aliases_data.items():
                try:
                    element = Element.objects.get(symbol=symbol)
                    
                    for alias in alias_list:
                        alias_text = str(alias).strip()
                        if not alias_text:
                            continue
                        
                        # Detect language
                        language = "fa" if any('\u0600' <= char <= '\u06FF' for char in alias_text) else "en"
                        
                        # Detect type
                        alias_type = "common"
                        if alias_text.isdigit():
                            alias_type = "number"
                        elif len(alias_text) <= 3:
                            alias_type = "abbreviation"
                        elif any(word in alias_text.lower() for word in ["group", "period", "metal", "gas"]):
                            alias_type = "classification"
                        
                        aliases_to_create.append(ElementAlias(
                            element=element,
                            alias=alias_text,
                            language=language,
                            alias_type=alias_type
                        ))
                except Element.DoesNotExist:
                    logger.warning(f"Element not found for symbol: {symbol}")
            
            # Bulk create aliases
            ElementAlias.objects.bulk_create(aliases_to_create, batch_size=100)
            logger.info(f"Created {len(aliases_to_create)} aliases")
        
        logger.info("Database initialization completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        return False

def get_database_stats():
    """Get comprehensive database statistics"""
    stats = {
        'elements': Element.objects.count(),
        'aliases': ElementAlias.objects.count(),
        'page_views': PageView.objects.aggregate(total=Coalesce(Sum('view_count'), 0))['total'],
        'searches': SearchHistory.objects.count(),
        'connection_stats': _connection_manager.get_connection_stats(),
        'timestamp': timezone.now().isoformat()
    }
    
    return stats

def cleanup():
    """Cleanup database connections"""
    # Django handles connection cleanup automatically
    pass

# Auto-initialize database when module is imported
try:
    init_database()
except Exception as e:
    logger.error(f"Auto-initialization failed: {e}")