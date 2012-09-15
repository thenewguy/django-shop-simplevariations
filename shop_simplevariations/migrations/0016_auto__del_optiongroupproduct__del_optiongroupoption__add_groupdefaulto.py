# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'OptionGroupProduct'
        db.delete_table('shop_simplevariations_optiongroupproduct')

        # Deleting model 'OptionGroupOption'
        db.delete_table('shop_simplevariations_optiongroupoption')

        # Adding model 'GroupDefaultOptionThrough'
        db.create_table('shop_simplevariations_groupdefaultoptionthrough', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_simplevariations.OptionGroup'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_simplevariations.Option'])),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('shop_simplevariations', ['GroupDefaultOptionThrough'])

        # Adding model 'GroupProductThrough'
        db.create_table('shop_simplevariations_groupproductthrough', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_simplevariations.OptionGroup'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('shop_simplevariations', ['GroupProductThrough'])


    def backwards(self, orm):
        # Adding model 'OptionGroupProduct'
        db.create_table('shop_simplevariations_optiongroupproduct', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop.Product'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_simplevariations.OptionGroup'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal('shop_simplevariations', ['OptionGroupProduct'])

        # Adding model 'OptionGroupOption'
        db.create_table('shop_simplevariations_optiongroupoption', (
            ('order', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_simplevariations.OptionGroup'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['shop_simplevariations.Option'])),
        ))
        db.send_create_signal('shop_simplevariations', ['OptionGroupOption'])

        # Deleting model 'GroupDefaultOptionThrough'
        db.delete_table('shop_simplevariations_groupdefaultoptionthrough')

        # Deleting model 'GroupProductThrough'
        db.delete_table('shop_simplevariations_groupproductthrough')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shop.cart': {
            'Meta': {'object_name': 'Cart'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'shop.cartitem': {
            'Meta': {'object_name': 'CartItem'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['shop.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {})
        },
        'shop.product': {
            'Meta': {'object_name': 'Product'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_shop.product_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        },
        'shop_simplevariations.cartitemoption': {
            'Meta': {'ordering': "('group', 'choice')", 'object_name': 'CartItemOption'},
            'cartitem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.CartItem']"}),
            'choice': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.OptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.Option']"})
        },
        'shop_simplevariations.cartitemtextoption': {
            'Meta': {'object_name': 'CartItemTextOption'},
            'cartitem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'text_option'", 'to': "orm['shop.CartItem']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.TextOption']"})
        },
        'shop_simplevariations.groupdefaultoptionthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'GroupDefaultOptionThrough'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.OptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.Option']"}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'shop_simplevariations.groupproductthrough': {
            'Meta': {'ordering': "['order']", 'object_name': 'GroupProductThrough'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.OptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop.Product']"})
        },
        'shop_simplevariations.option': {
            'Meta': {'object_name': 'Option'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.OptionGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'})
        },
        'shop_simplevariations.optiongroup': {
            'Meta': {'object_name': 'OptionGroup'},
            'choose_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'defaults': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['shop_simplevariations.Option']", 'null': 'True', 'through': "orm['shop_simplevariations.GroupDefaultOptionThrough']", 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['shop.Product']", 'null': 'True', 'through': "orm['shop_simplevariations.GroupProductThrough']", 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'subgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shop_simplevariations.OptionGroup']", 'null': 'True', 'blank': 'True'})
        },
        'shop_simplevariations.textoption': {
            'Meta': {'object_name': 'TextOption'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '12', 'decimal_places': '2'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'text_options'", 'symmetrical': 'False', 'to': "orm['shop.Product']"}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['shop_simplevariations']